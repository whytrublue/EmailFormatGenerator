import streamlit as st
import pandas as pd
from urllib.parse import urlparse

# Email format templates
email_formats = [
    "{first}.{last}@{domain}",
    "{first[0]}.{last}@{domain}",
    "{first}.{last[0]}@{domain}",
    "{first[0]}.{last[0]}@{domain}",
    "{last}.{first}@{domain}",
    "{last}.{first[0]}@{domain}",
    "{first}_{last}@{domain}",
    "{first}@{domain}",
    "{last}@{domain}",
    "{first}{last}@{domain}",
    "{first[0]}{last}@{domain}",
    "{first}{last[0]}@{domain}",
]

st.title("Email Format Generator")

# Input section
full_name = st.text_input("Enter Full Name (e.g., John Smith)")
domain_input = st.text_input("Enter Website/Domain (e.g., www.google.com)")

if full_name and domain_input:
    try:
        # Split name
        name_parts = full_name.strip().split()
        first = name_parts[0].lower()
        last = name_parts[-1].lower() if len(name_parts) > 1 else ""

        # Extract domain from full URL
        parsed = urlparse(domain_input if domain_input.startswith("http") else f"http://{domain_input}")
        domain = parsed.netloc or parsed.path
        domain = domain.replace("www.", "").strip().lower()

        # Generate emails
        emails = []
        for fmt in email_formats:
            try:
                email = fmt.format(first=first, last=last, domain=domain)
                emails.append(email)
            except Exception:
                continue

        # Display result
        df = pd.DataFrame({"Generated Emails": emails})
        st.dataframe(df)

        # Download
        csv = df.to_csv(index=False)
        st.download_button("Download as CSV", csv, "emails.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {e}")
