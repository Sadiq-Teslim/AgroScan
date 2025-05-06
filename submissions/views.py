import requests
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import PlantDiagnosis
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@login_required
@csrf_exempt  # Only use this if CSRF is handled manually or via tokens (e.g. in JS)
def run_diagnosis(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        image_prompt = request.POST.get('notes', '')

        if not image_file:
            return JsonResponse({'error': 'No image file provided'}, status=400)

        try:
            # Prepare payload for AI API
            api_url = 'https://example-ai-api.com/analyze'
            files = {'image': image_file}
            data = {'text': image_prompt} if image_prompt else {}

            # Make request to AI
            response = requests.post(api_url, files=files, data=data)
            response.raise_for_status()
            ai_data = response.json()

            # Save response to DB
            diagnosis = PlantDiagnosis.objects.create(
                user=request.user,
                image=image_file,
                image_prompt=image_prompt,
                diagnosis_title=ai_data.get('diagnosis_title', 'Untitled'),
                health_condition=ai_data.get('health_condition', 'Unknown'),
                disease_signs=ai_data.get('disease_signs', 'None detected'),
                control_suggestions=ai_data.get('control_suggestions', 'None provided'),
                summary=ai_data.get('summary', 'No summary available'),
            )

            return JsonResponse({
                'message': 'Diagnosis saved successfully',
                'data': {
                    'diagnosis_title': diagnosis.diagnosis_title,
                    'health_condition': diagnosis.health_condition,
                    'disease_signs': diagnosis.disease_signs,
                    'control_suggestions': diagnosis.control_suggestions,
                    'summary': diagnosis.summary,
                    'image_url': diagnosis.image.url,
                    'created_at': diagnosis.created_at.isoformat(),
                }
            }, status=201)

        except requests.RequestException as e:
            return JsonResponse({'error': f'Failed to connect to AI API: {str(e)}'}, status=502)
        except ValueError:
            return JsonResponse({'error': 'Invalid JSON response from AI'}, status=500)

    return JsonResponse({'error': 'Only POST method allowed'}, status=405)
