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

st.title("Flexible Email Format Generator")

# Input fields
full_name = st.text_input("Enter Full Name (e.g., John Smith)")
domain_input = st.text_input("Enter Domain/URL (e.g., google.com, https://www.google.com)")

if full_name and domain_input:
    try:
        # Split name into first and last
        name_parts = full_name.strip().split()
        first = name_parts[0].lower()
        last = name_parts[-1].lower() if len(name_parts) > 1 else ""

        # Clean and extract domain using tldextract
        extracted = tldextract.extract(domain_input.strip())
        if extracted.domain and extracted.suffix:
            domain = f"{extracted.domain}.{extracted.suffix}"
        else:
            st.error("Could not extract domain. Please check your input.")
            st.stop()

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
        st.error(f"Something went wrong: {e}")
