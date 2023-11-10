import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import PyPDF2

# Initialize spaCy
nlp = spacy.load('en_core_web_sm')

# Define a function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() if page.extract_text() else ''
    return text

# Define a function to preprocess text
def preprocess(text):
    # Parse the text with spaCy
    doc = nlp(text)
    
    # Tokenize and lemmatize the text, filtering out stop words and punctuation,
    # and preserving words that are upper case (like SQL, PHP, C, etc.)
    tokens = [token.lemma_.lower() if not token.is_upper else token.lemma_
              for token in doc
              if not token.is_stop and not token.is_punct and not token.is_space]
    
    # Join the tokens back into a string
    return " ".join(tokens)

# Define job description and preprocess it
job_description = """
Intern Computer Science Student - Java Focus

Responsibilities:
- Assist in the development and maintenance of Java applications.
- Collaborate with senior developers and team members on software design.
- Participate in code reviews and adhere to software development best practices.
- Contribute to the development of internal tools and user-facing features.
- Engage in troubleshooting and debugging of Java applications.

Requirements:
- Currently pursuing a degree in Computer Science or a related field.
- Proficient in Java programming.
- Understanding of object-oriented programming principles.
- Familiarity with software development lifecycle and version control systems.
- Strong problem-solving skills and attention to detail.
- Eagerness to learn new technologies and methodologies.

Desirable Skills:
- Experience with web frameworks like Spring or Hibernate.
- Knowledge of database systems and SQL.
- Familiarity with front-end technologies (JavaScript, HTML, CSS) is a plus.
"""

job_description_processed = preprocess(job_description)

# List of paths to PDF resumes - replace these with actual file paths
pdf_paths = ["Resume_JiaJean.pdf", "Resume_LeeYikSeng.pdf", "Wong Sau Xuan- Internship - Resume.pdf"]

# Load and preprocess resumes
resumes_processed = [preprocess(extract_text_from_pdf(path)) for path in pdf_paths]

# Initialize the vectorizer
vectorizer = TfidfVectorizer(ngram_range=(1, 3))

# Fit the vectorizer on the preprocessed job description and resumes
vectorizer.fit([job_description_processed] + resumes_processed)

# Transform the job description and resumes into vectors
job_vector = vectorizer.transform([job_description_processed])
resume_vectors = vectorizer.transform(resumes_processed)

# Compute the cosine similarity
similarities = cosine_similarity(job_vector, resume_vectors)

# Decide on a pass/fail threshold - this may need to be adjusted
threshold = 0.05  # This threshold is arbitrary and can be adjusted
pass_fail = ["Pass" if score >= threshold else "Fail" for score in similarities[0]]

# Rank passing resumes
ranking = sorted(
    [(index, score, pass_fail[index]) for index, score in enumerate(similarities[0])],
    key=lambda x: -x[1]
)

# Print results
for rank, (index, score, result) in enumerate(ranking):
    print(f"Resume {index + 1}: Score = {score:.2f}, Result = {result}, Rank = {rank + 1}")

# for path in pdf_paths:
#     # Extract text for the current resume PDF
#     extracted_text = extract_text_from_pdf(path)
#     print(f"Extracted Text for {path}:", extracted_text)
    
#     # Preprocess the extracted text
#     preprocessed_text = preprocess(extracted_text)
#     print(f"Preprocessed Text for {path}:", preprocessed_text)
