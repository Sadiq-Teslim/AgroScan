# AgroScan API Documentation

## Diagnosis Endpoints

### POST /api/diagnose
Processes an image to diagnose plant diseases.

**Request:**
- Content-Type: multipart/form-data
- Body: file (image file)

**Response:**
```json
{
  "class": "Tomato_Early_blight",
  "confidence": 0.92
}