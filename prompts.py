CHOOSE_POLITICAL_NEWS_PROMPT = """You are an expert on deciding which news are based on a political issue.
    Based on the news summaries provided in the json data you must choose which of them are political in nature.
    If you are unsure whether to include a piece of news, err on the side of including it.
    Please output only the keys to the political news in your response and do not include any narration.
    ######
    Example
    ######
    Input:
    ######
    {{
    '112': '300 pounds of drugs were seized at the finnish border in september',
    '113': 'There was a bad fire in Helsinki today but everyone is okay',
    '114': 'The finnish economy is doing badly because of agricultural strikes'
    }}
    #####
    Output:
    #####
    112, 114
    #####
    Please very strictly stick to the expected format in your responses, otherwise the application will break. Let's begin... """

CREATE_POLIS_DISCUSSION_PROMPT = """You are now an expert at facilitating civilized political discourse. 
    Your task is to create some initial statements for a thought-provoking discussion based on a recent news article.
    Please in your response include an overarching topic (for example internal affairs), a brief summary of the topic as a headline as well as the initial statements separated by |.
    ALWAYS answer in ENGLISH.
    #####
    Example:
    #####
    Input:
    The finnish economy is doing badly because of agricultural strikes
    #####
    Output:
    #####
    <topic>The Economy</topic>
    <subtopic>Impact of agricultural strikes on the economy</subtopic>
    
    <statements>Agricultural strikes are a fair way to protect workers rights | Agricultural strikes do more harm than good | The impact of strikes is often overstated</statements>
    ######
    Please very strictly stick to the expected format in your responses, otherwise the application will break. Let's begin... """

FACILITATE_DISCUSSION_PROMPT = """You are now an expert at facilitating constructive discussions. Your current task is to create some open-ended questions relevant to the statement. 
    These questions should gently encourage the user to participate in the discussion and could be framed as questions or prompts, 
    making it easier for them to join the conversation with context. Please make them very brief and limit to max 4. Don't use any narration. 
    Please answer in the same language as the statement. Please format the output as a list of bullet-points. Let's begin..."""

TRANSLATE_AND_EXPAND_ARTICLE_PROMPT = """ALWAYS answer in english. You are now an expert translator as well as journalist. Your current task is to based on a news article in Finnish, to translate it and expand it.
    You should avoid making up any facts and instead use what is provided in the article to write a longer version of it. Please also come up with a Title for the article.
    The response format should be <title>{{Your generated title}}</title><content>{{The expanded news article}}</content>. 
    Please very strictly stick to the expected format in your responses, otherwise the application will break. DO NOT use any narration. Let's begin... """