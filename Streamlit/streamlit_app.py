
from st_on_hover_tabs import on_hover_tabs
from PIL import Image
import streamlit as st
import pandas as pd
import numpy as np
import joblib

st.set_page_config(layout='wide')

st.header('Welcome to Assessifier!')
st.markdown('<style>' + open('./style.css').read() + '</style>', unsafe_allow_html=True)


# Define custom styles for tabs, including active tab style
custom_tab_styles = {
    'navtab': {
        'background-color': '#01427a',
        'color': '#818181',
        'font-size': '18px',
        'transition': '.3s',
        'white-space': 'normal',
        'text-transform': 'uppercase'
    },
    'tabOptionsStyle': {
        'color': 'white',
    },
    'iconStyle': {
        'position': 'fixed',
        'left': '7.5px',
        'text-align': 'left'
    },
    'tabStyle': {
        'list-style-type': 'none',
        'margin-bottom': '30px',
        'padding-left': '30px'
    },
}

with st.sidebar:
    tabs = on_hover_tabs(
        tabName=['Home', 'Exploratory Data Analysis', 'About', 'Documentation'],
        iconName=['home', 'insert_chart', 'info', 'description'],
        default_choice=0,
        styles=custom_tab_styles,
        key='1'
    )

# Functions
def questions():
    # Create an empty dictionary to store responses
    responses_dict = {'Question': [], 'Answer': []}
    
    demographics_questions = {
        'Gender': ['Female', 'Male'],
        'Level of Study': ['Certificate/Diploma', 'Undergraduate', 'Postgraduate']
    }
    
    st.subheader('Demographics:')
    for question, options in demographics_questions.items():
        selected_option = st.radio(question, options)
        responses_dict['Question'].append(question)
        responses_dict['Answer'].append(selected_option)
        
#     preference_questions = {
# #         'Preferred learning mode': ['Face to Face', 'Asynchronous Online Learning (On your own time)', 
# #                                     'Synchronous Online Learning (Real Time)'],
# #         'Preferred Social Media Platform':['Facebook', 'Blogger/Wordpress', 'Instagram', 'Twitter', 'Youtube', 'Others'],
#         'Preferred Communication Platform':['Call', 'Email', 'University eLearning Chat Room',
#                                            'Whatsapp', 'Others']
# #         'Difficulties in Online Learning':['Adaptability', 'Technical Issues', 'Computer Literacy', 'Time Management', 'Self-Motivation',
# #                                            'Quality of Material', 'Engagement', 'Accessibility', 'Cost', 'Focus/Commitment', 
# #                                            'Health Issues']
#     }
        
    st.subheader('Preferred Communication Platform')
    selected_option = st.multiselect('Select all options that apply.', ['Email', 'University eLearning Chat Room',
                                                                        'Whatsapp', 'Call', 'Telegram', 'Others'])
#     responses_dict['Question'].append('Preferred Communication Platform')
#     responses_dict['Answer'].append(', '.join(selected_option))
    if not selected_option:
        st.error('Please select at least 1 option.')
    else: 
        responses_dict['Question'].append('Preferred Communication Platform')
        responses_dict['Answer'].append(', '.join(selected_option))
           
#     for question, options in preference_questions.items():
#         selected_option = st.multiselect(question, options)
#         responses_dict['Question'].append(question)
#         responses_dict['Answer'].append(', '.join(selected_option))
    
    vak_questions = {
        '1. When operating new equipment for the first time I prefer to': ['Read the instructions', 'Listen to or ask for an explaination', 
                                                                           'Have a go and learn by \'trial and error\''],
        '2. When seeking travel directions I': ['Look at a map', 'Ask for spoken directions', 'Follow my nose or maybe use a compass'],
        '3. When cooking a new dish I': ['Follow a recipe', 'Call a friend for explaination', 'Follow my instinct, tasting as I cook'],
        '4. To teach someone something I': ['Write Instructions', 'Explain verbally', 'Demonstrate and let them have a go'],
        '5. I tend to say': ['I see what you mean', 'I hear what you are saying', 'I know how you feel'],
        '6. I tend to say': ['Show me', 'Tell me', 'Let me try'],
        '7. I tend to say': ['Watch how I do it', 'Listen to me explain', 'You have a go'],
        '8. Complaining about faulty goods I tend to': ['Write a letter', 'Phone', 
                                                        'Go back to the store, or send the faulty item to the head office'],
        '9. I prefer these leisure activities': ['Museums or galleries', 'Music or conversation', 'Physical activities or making things'],
        '10. When shopping generally I tend to': ['Look and decide', 'Discuss with shop staff', 'Try on, handle or test'],
        '11. Choosing a holiday I': ['Read the brochures', 'Listen to recommendations', 'Imagine the experience'],
        '12. Choosing a new car I': ['Read the reviews', 'Discuss with friends', 'Test-drive what you fancy'],
        '13. Learning a new skill': ['I watch what the teacher is doing', 
                                     'I talk through with the teacher exactly what I am supposed to do', 
                                     'I like to give it a try and work it out as I go along by doing it'],
        '14. Choosing from a restaurant menu': ['I imagine what the food will look like', 'I talk through the options in my head', 
                                                'I imagine what  the food will taste like'],
        '15. When listening to a band': ['I sing along to the lyrics (in my head or out loud)', 
                                         'I listen to the lyrics and the beats', 'I move in time with the music'],
        '16. When concentrating I': ['Focus on the words or pictures in front of me', 
                                     'Discuss the problem and possible solutions in my head', 
                                     'Move around a lot, fiddle with pens and pencils and touch unrelated things'],
        '17. I remember things best by': ['Writing notes or keeping printed details', 
                                          'Saying them aloud or repeating words and key points in my head', 
                                          'Doing and practicing the activity or imagining it being done'],
        '18. My first memory is of': ['Looking at something', 'Being spoken to', 'Doing something'],
        '19. When anxious I': ['Visualize the worst case scenarios', 'Talk over in my head what worries me most', 
                               'Can\'t sit still, fiddle and move around constantly'],
        '20. I feel especially connected to others because of': ['How they look', 'What they say to me', 'How they make me'],
        '21. When I revise for an exam, I': ['Write lots of revision notes', 'I talk over my notes, to myself or to other people', 
                                             'Imagine making the movement or creating the formula'],
        '22. When explaining something to someone, I tend to': ['Show them what I mean', 
                                                                'Explain to them in different ways until they understand', 
                                                                'Encourage them to try and talk them through the idea as they try'],
        '23. My main interests are': ['Photography or watching films or people watching', 
                                      'Listening to music or listening to the radio or talking to friends', 
                                      'Physical/sports activities or fine wines, fine foods or dancing'],
        '24. Most of my free time is spent': ['Watching television', 'Talking to friends', 'Doing physical activity or making things'],
        '25. When I first contact a new person': ['I arrange a face to face meeting', 'I talk to them on the telephone', 
                                                  'I try to get together to share an activity'],
        '26. I first notice how people': ['Look and dress', 'Sound and speak', 'Stand and move'],
        '27. If I am very angry': ['I keep replaying in my mind what it is that has upset me', 'I shout lots and tell people how I feel', 
                                   'I stomp about, slam doors and throw things'],
        '28. I find it easiest to remember': ['Faces', 'Names', 'Things I have done'],
        '29. I think I can tell someone is lying because': ['They avoid looking at you', 'Their voice changes', 
                                                            'The vibes I get from them'],
        '30. When I\'m meeting with an old friend': ['I say \"it\'s great to see you!\"', 'I say "it\'s great to hear your voice!"', 
                                                     'I give them a hug or a handshake']
    }
    
    st.subheader('The VAK Learning Styles Questions:')
    for question, options in vak_questions.items():
        selected_option = st.radio(question, options)
        responses_dict['Question'].append(question)
        responses_dict['Answer'].append(selected_option)
    
    if st.button('Submit'):
        # Convert the dictionary to a DataFrame
        responses_df = pd.DataFrame(responses_dict).transpose().reset_index()
        responses_df.columns = responses_df.iloc[0]  # Use the first row as column names
        responses_df = responses_df[1:]  # Skip the first row
        responses_df.drop(columns=['Question'], inplace=True, axis=1)

#         # Display the DataFrame
#         st.subheader('User Responses:')
#         st.write(responses_df)
        
        # Save into a new csv
        responses_df.to_csv('responses_st_dominantVAK.csv', index=False)
        st.session_state.csv_exists = True
        
        return responses_df


def get_dominant_vak(df):
    # Define answers options
    visual_keywords = ["Read the instructions", 
                   "Look at a map", 
                   "Follow a recipe", 
                   "Write Instructions",
                   "I see what you mean",
                   "Show me",
                   "Watch how I do it",
                   "Write a letter",
                   "Museums or galleries",
                   "Look and decide",
                   "Read the brochures",
                   "Read the reviews",
                   "I watch what the teacher is doing",
                   "I imagine what the food will look like",
                   "I sing along to the lyrics (in my head or out loud)",
                   "Focus on the words or pictures in front of me",
                   "Writing notes or keeping printed details",
                   "Looking at something",
                   "Visualize the worst case scenarios",
                   "How they look",
                   "Write lots of revision notes",
                   "Show them what I mean",
                   "Photography or watching films or people watching",
                   "Watching television",
                   "I arrange a face to face meeting",
                   "Look and dress",
                   "I keep replaying in my mind what it is that has upset me",
                   "Faces",
                   "They avoid looking at you",
                   "I say \"it's great to see you!\"",
                  ]

    auditory_keywords = ["Listen to or ask for an explaination", 
                     "Ask for spoken directions", 
                     "Call a friend for explaination",
                     "Explain verbally",
                     "I hear what you are saying",
                     "Tell me",
                     "Listen to me explain",
                     "Phone",
                     "Music or conversation",
                     "Discuss with shop staff",
                     "Listen to recommendations",
                     "Discuss with friends",
                     "I talk through with the teacher exactly what I am supposed to do",
                     "I talk through the options in my head",
                     "I listen to the lyrics and the beats",
                     "Discuss the problem and possible solutions in my head",
                     "Saying them aloud or repeating words and key points in my head",
                     "Being spoken to",
                     "Talk over in my head what worries me most",
                     "What they say to me",
                     "I talk over my notes, to myself or to other people",
                     "Explain to them in different ways until they understand",
                     "Listening to music or listening to the radio or talking to friends",
                     "Talking to friends",
                     "I talk to them on the telephone",
                     "Sound and speak",
                     "I shout lots and tell people how I feel",
                     "Names",
                     "Their voice changes",
                     "I say \"it's great to hear your voice!\""
                    ]

    kinesthetic_keywords = ["Have a go and learn by \"trial and error\"", 
                        "Follow my nose or maybe use a compass", 
                        "Follow my instinct, tasting as I cook",
                        "Demonstrate and let them have a go",
                        "I know how you feel",
                        "Let me try",
                        "You have a go",
                        "Go back to the store, or send the faulty item to the head office",
                        "Physical activities or making things",
                        "Try on, handle or test",
                        "Imagine the experience",
                        "Test-drive what you fancy",
                        "I like to give it a try and work it out as I go along by doing it",
                        "I imagine what the food will taste like", #double spacing here
                        "I move in time with the music",
                        "Move around a lot, fiddle with pens and pencils and touch unrelated things",
                        "Doing and practicing the activity or imagining it being done",
                        "Doing something",
                        "Can't sit still, fiddle and move around constantly",
                        "How they make me",
                        "Imagine making the movement or creating the formula",
                        "Encourage them to try and talk them through the idea as they try",
                        "Physical/sports activities or fine wines, fine foods or dancing",
                        "Doing physical activity or making things",
                        "I try to get together to share an activity",
                        "Stand and move",
                        "I stomp about, slam doors and throw things",
                        "Things I have done",
                        "The vibes I get from them",
                        "I give them a hug or a handshake"
                       ]
    
    ques_df = df.iloc[:, 7:37]
    
    visual_count = 0
    auditory_count = 0
    kinesthetic_count = 0

    # Iterate through the columns (each column is a question)
    for column in ques_df.columns:
        response = str(ques_df[column]).lower()
        
        # compare answer with the response
        for answer in visual_keywords:
            if answer.lower() in response:
                visual_count += 1

        for answer in auditory_keywords:
            if answer.lower() in response:
                auditory_count += 1

        for answer in kinesthetic_keywords:
            if answer.lower() in response:
                kinesthetic_count += 1

    # Determine the dominant VAK preference for this respondent
    preferences = {
        'Visual': visual_count,
        'Auditory': auditory_count,
        'Kinesthetic': kinesthetic_count
    }

    dominant_preference = max(preferences, key=preferences.get)
    
    # Add the list of dominant learning style as a new column in the DataFrame
    df['Dominant_VAK'] = dominant_preference
    
#     # Display the DataFrame
#     st.subheader('Dominat VAK:')
#     st.write(df)
    
    return df

def encode_responses(df):
    # Split multi-responses into different rows
    df['Preferred Communication Platform'] = df['Preferred Communication Platform'].str.split(', ')
    df = df.explode('Preferred Communication Platform')

    # Reset index after exploding
    df = df.reset_index(drop=True)
    
    # Define the custom ordinal encoding mapping
    gender_mapping = {
        'Female': 0,
        'Male': 1
    }

    study_level_mapping = {
        'Certificate/Diploma': 1,
        'Undergraduate': 2,
        'Postgraduate': 3
    }

    vak_mapping = {
        'Visual': 1,
        'Auditory': 2,
        'Kinesthetic': 3
    }
    
    df['Gender'] = df['Gender'].map(gender_mapping)
    df['Level of Study'] = df['Level of Study'].map(study_level_mapping)
    df['Dominant_VAK'] = df['Dominant_VAK'].map(vak_mapping)
    
    # One-hot encoding
    columns_to_encode = ['Preferred Communication Platform']
    df = pd.get_dummies(df, columns=columns_to_encode, prefix=columns_to_encode)
    
    # Extract VAK questions columns
    vak_ques_columns = df.iloc[:, 2:32]
    df = pd.get_dummies(df, columns=vak_ques_columns.columns, prefix=vak_ques_columns.columns)
    
    # To validate that the encoding is correct
    df.to_csv('encoded_responses.csv', index=False)
    # Mark that the CSV file already exists
    st.session_state.csv_exists = True
    
    return df

# Convert list into daatframe whereevery element in a list is a new row
def list_to_df(lst):
    # A. Convert list (containing lists in list) into a dataframe
    # Step 1: Create a DataFrame with a single column containing the list of lists
    df_initial = pd.DataFrame({'Online Assessment': [lst]})
    
    # Step 2: Use explode to flatten the list of lists
    df_exploded = df_initial.explode('Online Assessment')
    
    # Step 3: Reset the index to get a continuous index
    final_df = df_exploded.reset_index(drop=True)
    
    # B. Convert each list in a row into a series and then concatenate them
    # Step 1: Use apply and pd.Series to convert each list into a series
    series_column = final_df['Online Assessment'].apply(pd.Series)
    
    # Step 2: Use stack to stack the resulting series, creating a multi-level index
    stacked_series = series_column.stack()
    
    # Step 3: Use reset_index(drop=True) to reset the index and drop the multi-level index to form the final df
    final_df = stacked_series.reset_index(drop=True)
    
    # Rename the column to 'Online Assessment'
    final_df = final_df.rename('Online Assessment')

    # Remove duplicate rows
    final_df = final_df.drop_duplicates()
    
    return final_df

def classification_model(df):
    # Encode user's responses
    df = encode_responses(df)
    
    # Transform the df such that is matches the expected df format of the trained model (no. and type of column present)
    # Read an empty df that consists of only the expected name and arrangement of columns
    df_format = pd.read_csv('model_format.csv')
    # Insert user's responses (df) into the df_format
    for col in df.columns:
        if col in df_format.columns:
            df_format[col] = df[col]
            
    # Replace null values with 'FALSE'
    df_format = df_format.fillna(False)
    
    #  To validate that the df format is correct
    df_format.to_csv("userDf_correct_format.csv", index=False)
    # Mark that the CSV file already exists
    st.session_state.csv_exists = True
    
    # Load the trained model
    classifier = joblib.load('Model/rf.joblib')
    
    # Make predictions based on user's responses
    predictions = pd.DataFrame({col: model.predict(df_format) for col, model in classifier.items()})
    
    # Define the assessment name to be displayed
    assessment_mapping = {
        '6. Online Instructional Strategies/Assessment [Demonstration]': 'Demonstration',
        '6. Online Instructional Strategies/Assessment [Digital Lab Experiments]': 'Digital Lab Experiments',
        '6. Online Instructional Strategies/Assessment [Forum]': 'Forum',
        '6. Online Instructional Strategies/Assessment [Case Study]': 'Case Study',
        '6. Online Instructional Strategies/Assessment [Concept Mapping]': 'Concept Mapping',
        '6. Online Instructional Strategies/Assessment [Real Time Online Exam]': 'Real Time Online Exam',
        '6. Online Instructional Strategies/Assessment [Individual Project/Assignment]': 'Individual Project/Assignment',
        '6. Online Instructional Strategies/Assessment [Group Project/Assignment]': 'Group Project/Assignment',
        '6. Online Instructional Strategies/Assessment [Online Quiz/Test - MCQ]': 'MCQ',
        '6. Online Instructional Strategies/Assessment [Online Quiz/Test - Essay]': 'Essay',
        '6. Online Instructional Strategies/Assessment [Online Quiz/Test - Open Book]': 'Open Book',
        '6. Online Instructional Strategies/Assessment [Peer Review Assessment Live Presentation]': 'Live Presentation',
        '6. Online Instructional Strategies/Assessment [Recorded Presentation]': 'Recorded Presentation'
    }
    
    # Initialize an empty list to store the assessment names for each row
    all_rows_final_assessment = []

    # Iterate through each row in the predictions DataFrame
    for index, row in predictions.iterrows():
        # Get the suggested online assessment method(s) for the current row where value == 1 (suggested)
        final_assessment = predictions.columns[row == 1].tolist()
    
        # Map the defined assessment name to each suggested online assessment method column
        final_assessment_mapped = [assessment_mapping.get(col, col) for col in final_assessment]
    
        # Append the list of assessment names for the current row to the list
        all_rows_final_assessment.append(final_assessment_mapped)

    final_df = list_to_df(all_rows_final_assessment)
    
    #  To validate that the df format is correct
    final_df.to_csv("check_online_assessment.csv", index=False)
    # Mark that the CSV file already exists
    st.session_state.csv_exists = True
    
    # Display the content in a list
    st.header("Best Online Assessment Tool(s):")
    for i, assessment in enumerate(final_df, start=1):
#         st.text(f"{i}. {assessment}")
        st.write(f"- {assessment}")



# Individual tabs
if tabs =='Home':
    st.title('Curious to know which assessment method is best for you based on your learning style?')
    st.write('Fill in the questionnaire now!')
    responses_df = questions()
    # Check if the DataFrame is not None before performing other functions to ensure the questions() is being called first
    if responses_df is not None:
        # Get the dominant learning style of the user
        responses_vak_df = get_dominant_vak(responses_df)
#         encoded_df = encode_responses(responses_vak_df)
        # Call the trained classification model function to make prediction
        if responses_vak_df is not None:
            # Convert the Dominant_VAK data to a list for point form
            points_list = responses_df['Dominant_VAK'].tolist()

            # Display the dominant VAK
            st.header("Dominant Learning Style:")
            for point in points_list:
                st.write(f"- {point}")
                if point == 'Visual':
                    # Load the image
                    image = Image.open("Images/visual.png")
                elif point == 'Auditory':
                    # Load the image
                    image = Image.open("Images/auditory.png")
                elif point == 'Kinesthetic':
                    # Load the image
                    image = Image.open("Images/kinesthetic.png")
                # Display the image with custom width and height
                st.image(image, caption='Source: Freepik', use_column_width="always")
                
            classification_model(responses_vak_df)
    

elif tabs == 'Exploratory Data Analysis':
    st.title('Exploratory Data Analysis')
    st.write('Below features the descriptive analyses of the dataset utilized for model training, presented through dashboards. It provides insights into demographics and the preferred online assessment tools for visual, auditory and kinesthetic learners.')
    st.write('\n')
    # Tableau Public embed code
    tableau_embed_code_demographic = """
    <div class='tableauPlaceholder' id='viz1702047201422' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;DS&#47;DSP-Demographics&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='DSP-Demographics&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;DS&#47;DSP-Demographics&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1702047201422');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='1427px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
"""
    # Embed Tableau Public visualization in Streamlit app
    st.components.v1.html(tableau_embed_code_demographic, height=600)
    
    # Tableau Public embed code
    tableau_embed_code_assessment = """
    <div class='tableauPlaceholder' id='viz1702046913809' style='position: relative'><noscript><a href='#'><img alt='Dashboard 2 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;DS&#47;DSP-Assessment-Preference&#47;Dashboard2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='DSP-Assessment-Preference&#47;Dashboard2' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;DS&#47;DSP-Assessment-Preference&#47;Dashboard2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1702046913809');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
"""
    # Embed Tableau Public visualization in Streamlit app
    st.components.v1.html(tableau_embed_code_assessment, height=600)

elif tabs == 'About':
    st.title('About')
    
    st.header('What is learning style?')
    st.write('''Learning style influences **how learners prefer to receive and process information**. According to Dag and Gecer (2009), “Learning Style” refers to the learning ways or preferences which are used to learn or remember new knowledge by the learner. For example, visual learners may excel better in assessments that involve diagramming whereas auditory learners may excel better in oral assessments while kinesthetic learners may excel better in hands-on practicals.''')
    
    st.write("""Previous research by Sharp et al.,2008 has established that the **VAK Learning Styles Model**, in which VAK stands for Visual, Auditory, and Kinesthetic, is **the most widely used** among the learning style assessment instruments **to classify the most common ways that people learn**. The **VAK Learning Styles uses 3 main sensory receivers** to determine a learner’s dominant learning style. They are:""")
    numbered_list = ['Sight (Visual)', 'Hearing (Auditory)', 'Movement (Kinesthetic)']
    for i, item in enumerate(numbered_list, start=1):
        st.write(f"{i}. {item}")
        
    st.subheader('Watch the video below to learn more about learning style!')

    # Embed YouTube video using HTML code
    video_html = f'<iframe width="560" height="315" src="https://www.youtube.com/embed/_IopcOwfsoU?si=IGeRv-KntvAqWlzq" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'

    # Display the embedded video
    st.markdown(video_html, unsafe_allow_html=True)
    
    st.write('\n\n')
        
    st.header('How learning style is related to assessment?')
    st.write("""**A research by Wickramasinghe and Hettiarachchi, 2017 explored the relationship among students’ learning styles, assessment methods, and students’ performances.** The study aims to identify the learning styles of students and observe how different assessment methods affect their performance. The survey results showed that there is a significant difference in the marks obtained in pre and post-assessments, suggesting that **students perform better in assessment methods that align with their learning styles. The study concludes that there is a relationship between students’ learning styles, assessment methods and their performances.**""")
    # Display link to the research paper
    st.markdown('[Read the Research Paper](https://www.researchgate.net/publication/316643710_Relationship_among_students\'_learning_styles_assessment_methods_and_students\'_performances)')
    
elif tabs == 'Documentation':
    st.title('Documentation')
    
    st.header('Quick Guide')
    steps_list = [
        'Click on the ‘Home’ tab to answer the questionnaire to identify your learning style and the online assessment tools that are best for you.', 
        'Click on the ‘Exploratory Data Analysis’ tab to see the preferred online assessment tools for most visual, auditory and kinesthetic learners.', 
        'Click on the ‘About’ tab to learn more about learning style and how learning style is related to assessment.',
        'Click on the ‘Documentation’ tab to view a brief functionality of the website and it is where you access the user manual document.']
    for i, item in enumerate(steps_list, start=1):
        st.write(f"{i}. {item}")
    
    # Display a link with custom text
    st.markdown('[Click here for a detailed user manual](https://docs.google.com/document/d/1fpi2nS_uHRcyqF-JSOt0kUWTns3av-IkE24wZRxoftA/edit?usp=sharing)')
    
    st.subheader('Home')
    st.write('The Home page contains a questionnaire for users to answer to find out their dominant learning style and which online assessment tools are best suited for them. There are a total of 33 questions for users to answer and it will take around 10 minutes to complete answering. The results will be displayed shortly on the same page after the \'Submit\' button has been clicked.')
    
    st.subheader('Exploratory Data Analysis')
    st.write('The Exploratory Data Analysis page contains the descriptive analysis of the dataset used to train the model. It gives an overview of the demographics and the preferred online assessment tools for visual, auditory and kinesthetic learners.')
    
    st.subheader('About')
    st.write('The About page contains information that provides users with a more comprehensive understanding of what learning style is and how learning style relates to assessment methods.')
    
    st.subheader('Documentation')
    st.write('The Documentation page provides a brief overview of what each tab contains.')
    
