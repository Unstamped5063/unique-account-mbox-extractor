import mailbox
import re
import os
from email.header import decode_header

try:
    from tqdm import tqdm
    use_tqdm = True
except ImportError:
    use_tqdm = False

def display_intro():
    print("\033[1;34m")
    print("************************************")
    print("*                                  *")
    print("*   Unique Account Mbox Extractor  *")
    print("*                                  *")
    print("************************************")
    print("\033[0m")

def decode_header_field(header_field):
    """Decodes an email header field into a string."""
    if header_field is None:
        return ''
    if isinstance(header_field, str):
        return header_field
    else:
        decoded_header = decode_header(header_field)
        header_str = ''
        for part in decoded_header:
            if isinstance(part[0], bytes):
                try:
                    header_str += part[0].decode(part[1] or 'utf-8')
                except (LookupError, UnicodeDecodeError):
                    header_str += part[0].decode('latin1')
            else:
                header_str += part[0]
        return header_str

def extract_primary_domain(domain):
    """Extracts the primary domain from a full domain name."""
    parts = domain.split('.')
    if len(parts) > 2:
        return '.'.join(parts[-2:])
    return domain

def normalize_url(url):
    """Normalizes URLs to extract the primary domain."""
    url = url.lower().strip()
    if url.startswith('http://'):
        url = url[7:]
    elif url.startswith('https://'):
        url = url[8:]
    if url.startswith('www.'):
        url = url[4:]
    return extract_primary_domain(url.split('/')[0])

def get_user_defined_patterns():
    default_patterns = [
        r'(verify|confirm|activation|welcome|register|sign up|order|purchase|subscription|account)'
    ]
    print("\033[1;33mCurrent regex pattern(s) for identifying account-related emails:\033[0m")
    for pattern in default_patterns:
        print(f"- {pattern}")
    
    user_choice = input("\033[1;36mDo you want to use the default pattern(s)? (y/n): \033[0m").strip().lower()
    if user_choice == 'n':
        user_patterns = input("\033[1;36mEnter your regex pattern(s) separated by commas: \033[0m").strip()
        return [p.strip() for p in user_patterns.split(',')]
    return default_patterns

def extract_unique_domains(mbox_file, account_patterns):
    # Compile regular expressions
    account_patterns = [re.compile(pattern) for pattern in account_patterns]
    
    # Initialize a set to store unique primary domains
    unique_primary_domains = set()
    
    # Open the mbox file
    mbox = mailbox.mbox(mbox_file)
    
    # Get the total number of messages
    total_messages = len(mbox)
    
    # Use tqdm for the progress bar if available
    email_iter = tqdm(mbox, total=total_messages, desc="Processing Emails", unit=" email") if use_tqdm else mbox
    
    for message in email_iter:
        # Get the email subject and decode it if necessary
        subject = decode_header_field(message['subject']).lower()
        
        body = ''
        if message.is_multipart():
            for part in message.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    break
        else:
            body = message.get_payload(decode=True)
        
        if body:
            body = body.decode('utf-8', errors='ignore').lower()
        
        # Check if the subject contains account-related keywords
        if any(pattern.search(subject) for pattern in account_patterns):
            # Extract email addresses from the 'From' and 'To' headers
            from_address = decode_header_field(message['from'])
            to_address = decode_header_field(message['to'])
            
            if from_address:
                from_email = re.search(r'[\w\.-]+@([\w\.-]+\.\w+)', from_address)
                if from_email:
                    primary_domain = extract_primary_domain(from_email.group(1))
                    unique_primary_domains.add(primary_domain)
            
            if to_address:
                to_email = re.search(r'[\w\.-]+@([\w\.-]+\.\w+)', to_address)
                if to_email:
                    primary_domain = extract_primary_domain(to_email.group(1))
                    unique_primary_domains.add(primary_domain)
    
    # Sort the unique primary domains alphabetically
    sorted_domains = sorted(unique_primary_domains)
    
    # Save the unique primary domains to a text file
    with open('unique_primary_domains.txt', 'w') as f:
        for domain in sorted_domains:
            f.write(domain + '\n')
    
    print(f'\033[1;32m{len(sorted_domains)} unique primary domains extracted and saved to unique_primary_domains.txt.\033[0m')

def main():
    display_intro()
    
    account_patterns = get_user_defined_patterns()
    
    # Check for .mbox files in the current directory
    mbox_files = [f for f in os.listdir('.') if f.endswith('.mbox')]
    
    if mbox_files:
        print("\033[1;33mFound the following .mbox file(s) in the current directory:\033[0m")
        for i, file in enumerate(mbox_files, start=1):
            print(f"{i}. {file}")
        
        use_found_mbox = input(f"\033[1;36mDo you want to use '{mbox_files[0]}'? (y/n): \033[0m").strip().lower()
        if use_found_mbox == 'y':
            mbox_file = mbox_files[0]
        else:
            mbox_file = input("\033[1;36mPlease enter the path to your .mbox file: \033[0m").strip()
    else:
        mbox_file = input("\033[1;36mPlease enter the path to your .mbox file: \033[0m").strip()
    
    extract_unique_domains(mbox_file, account_patterns)

if __name__ == "__main__":
    main()
