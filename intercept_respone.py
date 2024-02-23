import json


async def intercept_response(response):
    if response.request.resource_type == 'xhr':
        try:
            data = await response.json()
            tweets_data = []

            entries = data.get('data', {}).get('user', {}).get('result', {}).get('timeline_v2', {}).get('timeline', {}).get('instructions', [])
            for instruction in entries:
                if instruction.get('type') == 'TimelineAddEntries':
                    for entry in instruction.get('entries', []):
                        tweet_content = entry.get('content', {}).get('itemContent', {}).get('tweet_results', {}).get('result', {})
                        if tweet_content:
                            full_text = tweet_content.get('legacy', {}).get('full_text', '')
                            conversation_id_str = tweet_content.get('legacy', {}).get('conversation_id_str', '')
                            created_at = tweet_content.get('legacy', {}).get('created_at', '')
                            tweets_data.append({
                                'full_text': full_text,
                                'conversation_id_str': conversation_id_str,
                                'created_at': created_at
                            })

            if tweets_data:
                with open('tweets_data.json', 'w') as f:
                    json.dump(tweets_data, f, indent=4)

        except Exception as e:
            print(f"Error processing response: {e}")
