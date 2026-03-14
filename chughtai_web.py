curl https://api.x.ai/v1/chat/completions \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer xai-TL9zC1XlpRDTaOeGJXy5V4dAazIejYuFhmplmBlS4gnuO5yTI3VeVwi90SP2aqDwVU1uG6D320LBERBh" \
    -d '{
      "messages": [
        {
          "role": "system",
          "content": "You are a test assistant."
        },
        {
          "role": "user",
          "content": "Testing. Just say hi and hello world and nothing else."
        }
      ],
      "model": "grok-4-latest",
      "stream": false,
      "temperature": 0
    }'
