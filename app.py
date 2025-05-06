import streamlit as st
import pandas as pd
import tldextract

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

# Input source
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
    pasted_text = st.text_area("Paste full name and domain separated by comma on each line (e.g., John Smith, google.com)", height=200)
    if pasted_text.strip():
        for line in pasted_text.strip().split("\n"):
            if "," in line:
                parts = line.strip().split(",", 1)
                name = parts[0].strip()
                domain = parts[1].strip()
                data.append([name, domain])

# Process and display results
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
        
        # Show the DataFrame table once
        st.dataframe(df_result)

        # CSV Download Button
        csv = df_result.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download CSV", data=csv, file_name="emails.csv", mime="text/csv")

        # Display emails in a code block for copying
        email_list = df_result["Generated Email"].tolist()
        email_text = "\n".join(email_list)
        st.subheader("Copy to Clipboard (Paste into Excel or Sheets)")
        st.code(email_text, language='text')  # Display the text in a code block for easy copying

    else:
        st.warning("No valid emails generated.")


elif option == "Paste Data":
    pasted_text = st.text_area("Paste full names (one per line) followed by the domain on the last line", height=300)
    if pasted_text.strip():
        lines = [line.strip() for line in pasted_text.strip().split("\n") if line.strip()]
        if len(lines) >= 2:
            domain = lines[-1]
            names = lines[:-1]
            for name in names:
                data.append([name, domain])
        else:
            st.warning("Please enter at least one name followed by a domain.")

