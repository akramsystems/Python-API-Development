# Python API Development

practising python api development

---

## CRUD Operations

### 1. Create [POST]

##### /posts

```python
@app.post("/posts")
```

---

### 2. Read [GET]

##### /posts/:id

```python
@app.get("/posts/{id}")
```

##### /posts

```python
@app.get("/posts")
```

---

### 3. Update [PUT/PATCH]

##### /posts/:id

```python
@app.put("/posts/{id}")
```

---

### 4. Delete [DELETE]

##### /posts/:id

```python
@app.delete("/posts/{id}")
```

---
