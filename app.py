"""
AI Policy Adaptation System
Course: LB3114 - BSc Applied Data Science Communication
Institution: General Sir John Kotelawala Defence University
"""

import streamlit as st
import os
from dotenv import load_dotenv

from utils.pdf_extractor import extract_text_from_pdf, count_words, get_word_frequency
from utils.summarizer import PolicySummarizer
from utils.policy_generator import PolicyGenerator
from config.scenarios import get_scenario_list, get_scenario_details

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Policy Adaptation System",
    page_icon="📜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .stat-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .stat-label {
        font-size: 0.9rem;
        color: #666;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'extracted_text' not in st.session_state:
    st.session_state.extracted_text = None
if 'summary' not in st.session_state:
    st.session_state.summary = None
if 'adapted_policy' not in st.session_state:
    st.session_state.adapted_policy = None
if 'summarizer' not in st.session_state:
    st.session_state.summarizer = None
if 'generator' not in st.session_state:
    st.session_state.generator = None

# Header
st.markdown('<div class="main-header">AI-Powered Policy Adaptation System</div>', 
            unsafe_allow_html=True)
st.markdown('<div class="sub-header">Transform Policy Documents Using Transformer Models & Advanced Prompt Engineering</div>', 
            unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("System Status")
    
    # Initialize models
    if st.session_state.summarizer is None:
        with st.spinner("Loading BART Summarizer..."):
            st.session_state.summarizer = PolicySummarizer()
    
    if st.session_state.generator is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            st.session_state.generator = PolicyGenerator(api_key)
            st.success("[OK] GPT Generator Ready")
        else:
            st.warning("[!] OpenAI API Key Missing")
            api_key_input = st.text_input("Enter OpenAI API Key:", type="password")
            if api_key_input:
                st.session_state.generator = PolicyGenerator(api_key_input)
                st.success("[OK] Generator Initialized")
    
    st.success("[OK] BART Summarizer Ready")
    
    st.divider()
    
    st.header("About")
    st.markdown("""
    **Technology Stack:**
    - Transformer Summarization (BART)
    - GPT-3.5 Policy Generation
    - Advanced Prompt Engineering
    
    **Capabilities:**
    - PDF/Text policy input
    - Structured summary output
    - Multi-scenario adaptation
    - Comparative analysis
    """)
    
    st.divider()
    
    st.header("Academic Info")
    st.markdown("""
    **Course:** LB3114  
    **Program:** BSc Applied Data Science Communication  
    **Institution:** General Sir John Kotelawala Defence University  
    **Intake:** 41
    """)

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Policy Summarization", 
    "Scenario-Based Adaptation",
    "Comparative Analysis",
    "Help & Guide"
])

# Tab 1: Policy Summarization
with tab1:
    st.header("Policy Document Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Upload Policy Document")
        st.info("**Supported:** PDF documents (text-based, not scanned images)\n\n"
                "**Recommended:** 5-50 pages for optimal processing\n\n"
                "**Tip:** Larger files may take longer to process")
        
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=['pdf'],
            help="Upload a policy document in PDF format"
        )
        
        if uploaded_file:
            if st.session_state.extracted_text is None or \
               st.session_state.get('current_file') != uploaded_file.name:
                
                with st.spinner("Extracting text from PDF..."):
                    text = extract_text_from_pdf(uploaded_file)
                    
                    if text:
                        st.session_state.extracted_text = text
                        st.session_state.current_file = uploaded_file.name
                        st.success(f"[OK] Successfully extracted {count_words(text):,} words")
                    else:
                        st.error("[ERROR] Failed to extract text. Please ensure the PDF contains selectable text.")
    
    with col2:
        if st.session_state.extracted_text:
            st.subheader("Document Statistics")
            
            word_count = count_words(st.session_state.extracted_text)
            
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{word_count:,}</div>
                <div class="stat-label">Total Words</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="stat-box">
                <div class="stat-number">{len(st.session_state.extracted_text):,}</div>
                <div class="stat-label">Characters</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Summarization options
    if st.session_state.extracted_text:
        st.divider()
        st.subheader("Summarization Configuration")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            method = st.selectbox(
                "Summarization Method",
                ["Extractive", "Abstractive", "Structured"],
                help="Extractive: Select key sentences\nAbstractive: Generate new summary\nStructured: Organized sections"
            )
        
        with col2:
            if method == "Extractive":
                num_sentences = st.slider("Number of Sentences", 3, 15, 5)
            else:
                max_length = st.slider("Maximum Length (words)", 100, 1000, 300)
        
        with col3:
            st.write("")  # Spacing
            st.write("")
            summarize_button = st.button("Generate Summary", type="primary", use_container_width=True)
        
        if summarize_button:
            with st.spinner(f"Generating {method.lower()} summary..."):
                summarizer = st.session_state.summarizer
                
                if method == "Extractive":
                    summary = summarizer.extractive_summarize(
                        st.session_state.extracted_text,
                        num_sentences=num_sentences
                    )
                    st.session_state.summary = {"text": summary}
                
                elif method == "Abstractive":
                    summary = summarizer.abstractive_summarize(
                        st.session_state.extracted_text,
                        max_length=max_length
                    )
                    st.session_state.summary = {"text": summary}
                
                else:  # Structured
                    summary = summarizer.structured_summarize(
                        st.session_state.extracted_text
                    )
                    st.session_state.summary = summary
                
                st.success("[OK] Summary generated successfully!")
        
        # Display summary
        if st.session_state.summary:
            st.divider()
            st.subheader("Generated Summary")
            
            if isinstance(st.session_state.summary, dict) and "main_goals" in st.session_state.summary:
                # Structured summary
                st.markdown("### Main Goals of the Policy")
                st.write(st.session_state.summary["main_goals"])
                
                st.markdown("### Key Measures & Strategies")
                st.write(st.session_state.summary["key_measures"])
                
                st.markdown("### Overall Direction")
                st.write(st.session_state.summary["overall_direction"])
            else:
                # Simple summary
                st.write(st.session_state.summary.get("text", st.session_state.summary))
            
            # Summary statistics
            st.divider()
            st.subheader("Summary Statistics")
            
            summary_text = st.session_state.summary.get("text", 
                           " ".join(st.session_state.summary.values()) if isinstance(st.session_state.summary, dict) else "")
            
            original_words = count_words(st.session_state.extracted_text)
            summary_words = count_words(summary_text)
            compression = ((original_words - summary_words) / original_words * 100) if original_words > 0 else 0
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Original Words", f"{original_words:,}")
            with col2:
                st.metric("Summary Words", f"{summary_words:,}")
            with col3:
                st.metric("Compression", f"{compression:.1f}%")
            with col4:
                st.metric("Reduction", f"{original_words/summary_words:.1f}x" if summary_words > 0 else "N/A")
            
            # Key terms
            st.subheader("Key Terms")
            word_freq = get_word_frequency(st.session_state.extracted_text, top_n=15)
            
            freq_text = " | ".join([f"**{word}** ({count})" for word, count in word_freq.items()])
            st.markdown(freq_text)

# Tab 2: Scenario-Based Adaptation
with tab2:
    st.header("Policy Adaptation by Scenario")
    
    if not st.session_state.summary:
        st.warning("[!] Please generate a policy summary first in the 'Policy Summarization' tab.")
    elif not st.session_state.generator or not st.session_state.generator.client:
        st.error("[ERROR] OpenAI API key not configured. Please add your API key in the sidebar or .env file.")
    else:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Select Adaptation Scenario")
            
            scenarios = get_scenario_list()
            selected_scenario = st.selectbox(
                "Choose a scenario",
                options=list(scenarios.keys()),
                format_func=lambda x: scenarios[x]
            )
            
            scenario_details = get_scenario_details(selected_scenario)
            
            if scenario_details:
                st.markdown(f"**{scenario_details['name']}**")
                st.write(scenario_details['description'])
                
                with st.expander("View Scenario Details"):
                    st.markdown("**Constraints:**")
                    for constraint in scenario_details['constraints']:
                        st.markdown(f"- {constraint}")
                    
                    st.markdown("**Priorities:**")
                    for priority in scenario_details['priorities']:
                        st.markdown(f"- {priority}")
                    
                    st.markdown(f"**Tone:** {scenario_details['tone']}")
                    st.markdown(f"**Target Audience:** {scenario_details['audience']}")
        
        with col2:
            st.subheader("Generation Settings")
            
            temperature = st.slider(
                "Creativity Level",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help="Lower = more focused, Higher = more creative"
            )
            
            max_tokens = st.slider(
                "Maximum Length (tokens)",
                min_value=500,
                max_value=3000,
                value=2000,
                step=100
            )
            
            additional_context = st.text_area(
                "Additional Context (optional)",
                placeholder="Add any specific requirements or context for this adaptation...",
                height=100
            )
        
        st.divider()
        
        if st.button("Generate Adapted Policy", type="primary", use_container_width=True):
            with st.spinner("Generating adapted policy... This may take 30-60 seconds..."):
                # Prepare summary text
                if isinstance(st.session_state.summary, dict):
                    if "text" in st.session_state.summary:
                        summary_text = st.session_state.summary["text"]
                    else:
                        summary_text = f"""
                        Main Goals: {st.session_state.summary.get('main_goals', '')}
                        
                        Key Measures: {st.session_state.summary.get('key_measures', '')}
                        
                        Overall Direction: {st.session_state.summary.get('overall_direction', '')}
                        """
                else:
                    summary_text = str(st.session_state.summary)
                
                # Generate adapted policy
                adapted = st.session_state.generator.generate_adapted_policy(
                    original_summary=summary_text,
                    scenario=scenario_details,
                    temperature=temperature,
                    max_tokens=max_tokens,
                    additional_context=additional_context
                )
                
                st.session_state.adapted_policy = {
                    'text': adapted,
                    'scenario': selected_scenario,
                    'scenario_name': scenario_details['name']
                }
                
                st.success("[OK] Adapted policy generated successfully!")
        
        # Display adapted policy
        if st.session_state.adapted_policy:
            st.divider()
            st.subheader(f"Adapted Policy: {st.session_state.adapted_policy['scenario_name']}")
            
            st.markdown(st.session_state.adapted_policy['text'])
            
            # Download button
            st.download_button(
                label="Download Adapted Policy",
                data=st.session_state.adapted_policy['text'],
                file_name=f"adapted_policy_{st.session_state.adapted_policy['scenario']}.txt",
                mime="text/plain"
            )

# Tab 3: Comparative Analysis
with tab3:
    st.header("Comparative Policy Analysis")
    
    if not st.session_state.summary:
        st.warning("[!] Please generate a policy summary first.")
    elif not st.session_state.adapted_policy:
        st.warning("[!] Please generate an adapted policy first.")
    elif not st.session_state.generator or not st.session_state.generator.client:
        st.error("[ERROR] OpenAI API key not configured.")
    else:
        st.info("Compare the original policy with the adapted version to understand key differences and changes.")
        
        if st.button("Generate Comparative Analysis", type="primary"):
            with st.spinner("Analyzing differences... This may take 30-60 seconds..."):
                # Prepare texts
                if isinstance(st.session_state.summary, dict):
                    if "text" in st.session_state.summary:
                        original_text = st.session_state.summary["text"]
                    else:
                        original_text = " ".join(st.session_state.summary.values())
                else:
                    original_text = str(st.session_state.summary)
                
                adapted_text = st.session_state.adapted_policy['text']
                scenario_name = st.session_state.adapted_policy['scenario_name']
                
                comparison = st.session_state.generator.compare_policies(
                    original=original_text,
                    adapted=adapted_text,
                    scenario_name=scenario_name
                )
                
                st.session_state.comparison = comparison
                st.success("[OK] Comparative analysis complete!")
        
        if st.session_state.get('comparison'):
            st.divider()
            st.subheader("Analysis Results")
            st.markdown(st.session_state.comparison)
            
            # Side-by-side comparison
            st.divider()
            st.subheader("Side-by-Side View")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("### Original Policy Summary")
                if isinstance(st.session_state.summary, dict):
                    if "text" in st.session_state.summary:
                        st.write(st.session_state.summary["text"])
                    else:
                        for key, value in st.session_state.summary.items():
                            st.markdown(f"**{key.replace('_', ' ').title()}:**")
                            st.write(value)
                else:
                    st.write(st.session_state.summary)
            
            with col2:
                st.markdown(f"### Adapted Policy ({st.session_state.adapted_policy['scenario_name']})")
                st.write(st.session_state.adapted_policy['text'])

# Tab 4: Help & Guide
with tab4:
    st.header("User Guide")
    
    st.markdown("""
    ## How to Use This System
    
    ### Step 1: Upload Policy Document
    1. Navigate to the **Policy Summarization** tab
    2. Upload a PDF document containing your policy
    3. The system will automatically extract and analyze the text
    
    ### Step 2: Generate Summary
    1. Choose your preferred summarization method:
       - **Extractive**: Selects the most important sentences from the original text
       - **Abstractive**: Uses AI to generate a new summary in different words
       - **Structured**: Organizes the summary into predefined sections
    2. Adjust settings (number of sentences or maximum length)
    3. Click "Generate Summary"
    
    ### Step 3: Adapt for Scenarios
    1. Go to the **Scenario-Based Adaptation** tab
    2. Select an adaptation scenario that fits your needs
    3. Adjust creativity and length settings
    4. Optionally add specific context or requirements
    5. Click "Generate Adapted Policy"
    
    ### Step 4: Compare Policies
    1. Visit the **Comparative Analysis** tab
    2. Generate a detailed comparison between original and adapted versions
    3. Review side-by-side differences
    
    ## Available Scenarios
    """)
    
    scenarios = get_scenario_list()
    for key, name in scenarios.items():
        details = get_scenario_details(key)
        with st.expander(name):
            st.write(f"**Description:** {details['description']}")
            st.write(f"**Target Audience:** {details['audience']}")
            st.write(f"**Tone:** {details['tone']}")
    
    st.divider()
    
    st.markdown("""
    ## Technical Information
    
    ### Models Used
    - **BART (facebook/bart-large-cnn)**: For text summarization
    - **GPT-3.5-turbo**: For policy adaptation and comparative analysis
    
    ### System Requirements
    - PDF documents must contain selectable text (not scanned images)
    - OpenAI API key required for policy adaptation features
    - Recommended document size: 5-50 pages
    
    ### Tips for Best Results
    1. **Clear PDFs**: Ensure your PDF has clear, extractable text
    2. **Relevant Context**: Provide specific context in the additional context field
    3. **Appropriate Scenarios**: Choose scenarios that match your actual use case
    4. **Iterative Refinement**: Try different creativity levels to find the best output
    
    ## Troubleshooting
    
    **Q: Summary generation is slow**  
    A: Large documents take longer to process. Consider documents under 50 pages for optimal performance.
    
    **Q: API key errors**  
    A: Ensure your OpenAI API key is correctly set in the `.env` file or entered in the sidebar.
    
    **Q: PDF text extraction fails**  
    A: Make sure your PDF contains selectable text, not scanned images. Use OCR software if needed.
    
    **Q: Generated policy seems off-topic**  
    A: Lower the creativity (temperature) setting and provide more specific context.
    
    ## Contact & Support
    For technical issues or questions about this system, please contact your course instructor.
    
    ---
    **Course:** LB3114 - BSc Applied Data Science Communication  
    **Institution:** General Sir John Kotelawala Defence University
    """)

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 2rem;'>
    <p><strong>AI Policy Adaptation System</strong></p>
    <p>Powered by Transformer Models & GPT | Course: LB3114</p>
    <p>© 2024 General Sir John Kotelawala Defence University</p>
</div>
""", unsafe_allow_html=True)