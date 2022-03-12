# Sentence Similarity 

### Install pipenv dependencies
```
pipenv install
```

### To run app
```
uvicorn app.main:app --reload
```

## Docker
### To make docker image

```
docker build -t sentencesimilarity .
```

### To run docker image
```
docker run -p 80:80 sentencesimilarity
```