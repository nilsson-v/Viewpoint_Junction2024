CHOOSE_POLITICAL_NEWS_PROMPT = """You are an expert on deciding which news are political.
    Based on the news summaries provided in the json data you must choose which of them are political in nature.
    Please output only the keys to the political news in your response and do not include any narration.
    ######
    Example
    ######
    Input:
    ######
    {{
    '112': 'Donald Trump will do some amazing work.',
    '113': 'There was a bad fire in Helsinki today but everyone is okay',
    '114': 'The finnish economy is doing badly because of agricultural strikes'
    }}
    #####
    Output:
    #####
    112, 114
    #####
    Please strictly stick to the expected format in your responses. Let's begin... """

CREATE_POLIS_DISCUSSION_PROMPT = ""