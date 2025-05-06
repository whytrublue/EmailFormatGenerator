import streamlit as st
import pandas as pd
import tldextract

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

st.title("Email Format Generator with Domain Extractor")

# Input section
full_name = st.text_input("Enter Full Name (e.g., John Smith)")
domain_input = st.text_input("Enter Website or Domain (e.g., https://www.google.co.uk)")

if full_name and domain_input:
    try:
        # Name processing
        name_parts = full_name.strip().split()
        first = name_parts[0].lower()
        last = name_parts[-1].lower() if len(name_parts) > 1 else ""

        # Use tldextract to get clean domain
        extracted = tldextract.extract(domain_input)
        if not extracted.domain or not extracted.suffix:
            st.error("Invalid domain input.")
        else:
            domain = f"{extracted.domain}.{extracted.suffix}"

            # Generate emails
            emails = []
            for fmt in email_formats:
                try:
                    email = fmt.format(first=first, last=last, domain=domain)
                    emails.append(email)
                except Exception:
                    continue

            # Display
            df = pd.DataFrame({"Generated Emails": emails})
            st.dataframe(df)

            # Download
            csv = df.to_csv(index=False)
            st.download_button("Download as CSV", csv, "emails.csv", "text/csv")

    except Exception as e:
        st.error(f"Error: {e}")
