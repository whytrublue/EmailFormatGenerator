import streamlit as st
import pandas as pd
import tldextract
import re

# Email format templates
email_formats = [
    "{first}.{last}@{domain}",
    "{first[0]}.{last}@{domain}",
    "{first}.{last[0]}@{domain}",
    "{first[0]}{last[0]}@{domain}",
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

st.title("Bulk Email Format Generator")

# Option selector
option = st.radio("Choose input method:", ("Upload CSV", "Paste Data"))

# Data holder
data = []

if option == "Upload CSV":
    uploaded_file = st.file_uploader("Upload CSV with 'Full Name' and 'Domain' columns", type=["csv"])
    if uploaded_file:
        df_input = pd.read_csv(uploaded_file)
        if 'Full Name' not in df_input.columns or 'Domain' not in df_input.columns:
            st.error("CSV must contain 'Full Name' and 'Domain' columns.")
        else:
            data = df_input[['Full Name', 'Domain']].values.tolist()

elif option == "Paste Data":
    pasted_text = st.text_area("Paste names followed by a domain (e.g., John Smith \\n Jane Doe \\n www.google.com)", height=300)
    if pasted_text.strip():
        lines = [line.strip() for line in pasted_text.strip().split("\n") if line.strip()]
        # Detect last line as domain if it looks like one
        domain_candidate = lines[-1]
        ext = tldextract.extract(domain_candidate)
        if ext.domain and ext.suffix:
            domain = f"{ext.domain}.{ext.suffix}"
            names = lines[:-1]
            data = [[name, domain] for name in names]
        else:
            st.error("Couldn't identify a valid domain in the last line.")

# Process and display
if data:
    all_emails = []

    for full_name, domain_input in data:
        name_parts = full_name.strip().split()
        if not name_parts:
            continue
        first = name_parts[0].lower()
        last = name_parts[-1].lower() if len(name_parts) > 1 else ""

        extracted = tldextract.extract(domain_input)
        if not extracted.domain or not extracted.suffix:
            continue
        domain = f"{extracted.domain}.{extracted.suffix}"

        for fmt in email_formats:
            try:
                email = fmt.format(first=first, last=last, domain=domain)
                all_emails.append({
                    "Full Name": full_name,
                    "Domain": domain,
                    "Email Format": fmt,
                    "Generated Email": email
                })
            except Exception:
                continue

    if all_emails:
        df_result = pd.DataFrame(all_emails)
        st.success(f"Generated {len(df_result)} emails.")
        st.dataframe(df_result)

        csv = df_result.to_csv(index=False)
        st.download_button("Download Results as CSV", csv, "emails.csv", "text/csv")
    else:
        st.warning("No valid emails generated.")

if all_emails:
    df_result = pd.DataFrame(all_emails)
    st.success(f"Generated {len(df_result)} emails.")
    st.dataframe(df_result)

    # Show just the generated emails for copy-paste
    email_list = df_result["Generated Email"].tolist()
    email_text = "\n".join(email_list)
    st.markdown("### 📋 Copy All Generated Emails")
    st.text_area("Click and press Ctrl+C or Cmd+C to copy", email_text, height=200)

    # Download button
    csv = df_result.to_csv(index=False)
    st.download_button("Download Results as CSV", csv, "emails.csv", "text/csv")

