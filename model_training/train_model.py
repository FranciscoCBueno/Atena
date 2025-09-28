import pandas as pd
import spacy
from nltk.corpus import stopwords
import string
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

nlp = spacy.load("pt_core_news_sm")
stop_words = stopwords.words('portuguese')
punctuations = string.punctuation

print("Carregando dados de 'Emails.csv'...")
df = pd.read_csv('Emails.csv') 

df['Assunto'] = df['Assunto'].fillna('')
df['Corpo'] = df['Corpo'].fillna('')
df['texto_completo'] = df['Assunto'] + " " + df['Corpo']
print(f"Dados carregados com sucesso! Total de {len(df)} exemplos.")

def preprocess_text(text):
    doc = nlp(text.lower())
    processed_tokens = [
        token.lemma_ 
        for token in doc 
        if token.is_alpha and token.lemma_ not in stop_words and token.lemma_ not in punctuations
    ]
    return " ".join(processed_tokens)

print("\nIniciando pré-processamento dos textos...")
df['texto_processado'] = df['texto_completo'].apply(preprocess_text)
print("Pré-processamento concluído.")

X = df['texto_processado']
y = df['Categoria']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LinearSVC())
])

print("\nIniciando treinamento do modelo...")
pipeline.fit(X_train, y_train)
print("Treinamento concluído.")

print("\nAvaliando o desempenho do modelo...")
y_pred = pipeline.predict(X_test)
print(f"\nAcurácia no conjunto de teste: {accuracy_score(y_test, y_pred):.2f}")
print("\nRelatório de Classificação:")
print(classification_report(y_test, y_pred))

model_filename = 'email_classifier_pipeline.pkl'
joblib.dump(pipeline, model_filename)
print(f"Modelo atualizado e salvo com sucesso como '{model_filename}'!")