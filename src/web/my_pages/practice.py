import streamlit as st
import pymongo
import time
import plotly.graph_objects as go
import os
import random
from datetime import datetime
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq

if "GROQ_API_KEY" not in os.environ:
    os.environ["GROQ_API_KEY"] = os.getenv("API_KEY")

TASK1_TOPICS = [
    "Population", "Economy", "Health", "Environment", "Education", "Technology", "Society", "Culture", "Politics"
]

TASK2_TOPICS = [
    "Education", "Technology", "Environment", "Health", "Society", "Economy", "Culture", "Politics"
]

TASK2_TOPICS_KEYWORDS = {
    "Education": ["school", "university", "student", "teacher", "curriculum", "learning", "knowledge", "degree", "training", "academic"],
    "Technology": ["digital", "internet", "device", "software", "hardware", "innovation", "communication", "information", "cyber", "network", "AI"],
    "Environment": ["climate", "pollution", "waste", "recycling", "sustainability", "conservation", "ecosystem", "green", "carbon", "emission"],
    "Health": ["medical", "disease", "treatment", "vaccine", "hospital", "doctor", "patient", "wellness", "nutrition", "exercise"],
    "Society": ["community", "culture", "tradition", "diversity", "equality", "justice", "social", "behavior", "norm", "value"],
    "Economy": ["market", "trade", "finance", "investment", "business", "industry", "employment", "income", "wealth", "growth"],
    "Culture": ["art", "music", "literature", "heritage", "tradition", "custom", "cultural", "creative", "expression", "identity"],
    "Politics": ["government", "policy", "election", "democracy", "power", "authority", "legislation", "administration", "political", "vote"],
}

TASK2_QUESTION_TYPES = [
    "Discuss both views and give your opinion.",
    "Discuss the advantages and disadvantages.",
]

llm1 = ChatGroq(
    model="llama3-groq-70b-8192-tool-use-preview",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

llm2 = ChatGroq(
    model="llama-3.1-70b-versatile",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
)

db_client = pymongo.MongoClient(os.getenv("MONGO_URL"))

class IELTSTask1Line(BaseModel):
    task1_description: str = Field(..., title="Task 1 Description", description="A detailed description of the IELTS Task 1, focusing on the interpretation of line graphs. Provide context, such as what the graph represents, the time period, and any key trends or changes that need to be discussed.")
    task1_line_data_category: list = Field(..., title="Task 1 Line Data Categories", description="List of categories for each line in the graph. Each category represents a different variable or dataset being compared, such as years, regions, or types of items.")
    task1_line_data_x: list = Field(..., title="Task 1 Line Data X-Axis", description="Data points for the x-axis. Typically, this would represent time or another continuous variable. Ensure the values correspond to the appropriate intervals shown in the graph.")
    task1_line_data_y: list[list] = Field(..., title="Task 1 Line Data Y-Axis", description="Y-axis data for multiple lines, with each list representing a line. Ensure the values have moderate differences, show multiple trends, and include several intersections between lines.")
    task1_line_x_y_labels: list = Field(..., title="Task 1 Line Data X and Y Labels", description="Labels for both the x-axis and y-axis, providing clear information about what each axis represents (e.g., 'Year', 'Population', 'Sales'). These labels help define the nature of the data presented on the graph.")

class IELTSTask2(BaseModel):
    task2_topic: str = Field(..., title="Task 2 Topic", description="The topic of the Task 2, e.g., 'Education', 'Technology', 'Environment', 'Health', 'Society', 'Economy', 'Culture', 'Politics', etc.")
    task2_question: str = Field(..., title="Task 2 Question", description="The question of the Task 2, You need point out the question and write an essay based on the question.")

class IELTSTask1_Criteria_Coherence_and_Cohesion(BaseModel):
    task1_criteria_coherence_and_cohesion: float = Field(..., title="Task 1 Criteria: Coherence and Cohesion", description="The score for the Coherence and Cohesion criteria in Task 1, which evaluates the logical flow of ideas and the connections between sentences and paragraphs.")
    task1_criteria_coherence_and_cohesion_feedback: str = Field(..., title="Task 1 Criteria: Coherence and Cohesion Feedback", description="Feedback on the Coherence and Cohesion criteria in Task 1, highlighting areas for improvement and suggestions for enhancing the overall coherence and cohesion of the essay.")

class IELTSTask1_Criteria_Lexical_Resource(BaseModel):
    task1_criteria_lexical_resource: float = Field(..., title="Task 1 Criteria: Lexical Resource", description="The score for the Lexical Resource criteria in Task 1, which assesses the range and accuracy of vocabulary used in the essay.")
    task1_criteria_lexical_resource_feedback: str = Field(..., title="Task 1 Criteria: Lexical Resource Feedback", description="Feedback on the Lexical Resource criteria in Task 1, indicating strengths and weaknesses in vocabulary usage and providing suggestions for expanding vocabulary and improving word choice.")

class IELTSTask1_Criteria_Grammatical_Range_and_Accuracy(BaseModel):
    task1_criteria_grammatical_range_and_accuracy: float = Field(..., title="Task 1 Criteria: Grammatical Range and Accuracy", description="The score for the Grammatical Range and Accuracy criteria in Task 1, which evaluates the variety and correctness of grammatical structures used in the essay.")
    task1_criteria_grammatical_range_and_accuracy_feedback: str = Field(..., title="Task 1 Criteria: Grammatical Range and Accuracy Feedback", description="Feedback on the Grammatical Range and Accuracy criteria in Task 1, highlighting grammatical errors and providing suggestions for improving sentence structure and accuracy.")

class IELTSTask1_Criteria_Task_Achievement(BaseModel):
    task1_criteria_task_achievement: float = Field(..., title="Task 1 Criteria: Task Achievement", description="The score for the Task Achievement criteria in Task 1, which assesses how well the essay addresses the question, presents relevant ideas, and supports arguments with examples and evidence.")
    task1_criteria_task_achievement_feedback: str = Field(..., title="Task 1 Criteria: Task Achievement Feedback", description="Feedback on the Task Achievement criteria in Task 1, indicating the effectiveness of addressing the question and providing suggestions for enhancing the clarity and relevance of the content.")

class IELTSTask2_Criteria_Task_Achievement(BaseModel):
    task2_criteria_task_achievement: float = Field(..., title="Task 2 Criteria: Task Achievement", description="The score for the Task Achievement criteria in Task 2, which assesses how well the essay addresses the question, presents relevant ideas, and supports arguments with examples and evidence.")
    task2_criteria_task_achievement_feedback: str = Field(..., title="Task 2 Criteria: Task Achievement Feedback", description="Feedback on the Task Achievement criteria in Task 2, indicating the effectiveness of addressing the question and providing suggestions for enhancing the clarity and relevance of the content.")

class IELTSTask2_Criteria_Coherence_and_Cohesion(BaseModel):
    task2_criteria_coherence_and_cohesion: float = Field(..., title="Task 2 Criteria: Coherence and Cohesion", description="The score for the Coherence and Cohesion criteria in Task 2, which evaluates the logical flow of ideas and the connections between sentences and paragraphs.")
    task2_criteria_coherence_and_cohesion_feedback: str = Field(..., title="Task 2 Criteria: Coherence and Cohesion Feedback", description="Feedback on the Coherence and Cohesion criteria in Task 2, highlighting areas for improvement and suggestions for enhancing the overall coherence and cohesion of the essay.")

class IELTSTask2_Criteria_Lexical_Resource(BaseModel):
    task2_criteria_lexical_resource: float = Field(..., title="Task 2 Criteria: Lexical Resource", description="The score for the Lexical Resource criteria in Task 2, which assesses the range and accuracy of vocabulary used in the essay.")
    task2_criteria_lexical_resource_feedback: str = Field(..., title="Task 2 Criteria: Lexical Resource Feedback", description="Feedback on the Lexical Resource criteria in Task 2, indicating strengths and weaknesses in vocabulary usage and providing suggestions for expanding vocabulary and improving word choice.")

class IELTSTask2_Criteria_Grammatical_Range_and_Accuracy(BaseModel):
    task2_criteria_grammatical_range_and_accuracy: float = Field(..., title="Task 2 Criteria: Grammatical Range and Accuracy", description="The score for the Grammatical Range and Accuracy criteria in Task 2, which evaluates the variety and correctness of grammatical structures used in the essay.")
    task2_criteria_grammatical_range_and_accuracy_feedback: str = Field(..., title="Task 2 Criteria: Grammatical Range and Accuracy Feedback", description="Feedback on the Grammatical Range and Accuracy criteria in Task 2, highlighting grammatical errors and providing suggestions for improving sentence structure and accuracy.")

def generate_task1_question(type: str = "line"):
    if type == "line":
        task1_llm = llm1.with_structured_output(IELTSTask1Line)
        random_topic = random.choice(TASK1_TOPICS)
        random_bias = random.choice([1, 10, 100, 1000])
        length = random.randint(3, 6)
        eg_list = [[random.randint(1, 10) for _ in range(length)] for _ in range(random.randint(2, 4))]
        eg_list_with_bias = [[x + random_bias for x in eg] for eg in eg_list]
        eg_list_with_bias_str = str(eg_list_with_bias).replace("[[", "[").replace("]]", "]")
        task1_question = task1_llm.invoke(f"Generate an IELTS Task 1 question on the topic of {random_topic}, In line data please provide several intersections between lines. e.g. {eg_list_with_bias_str}.")

    return task1_question, type

def generate_task2_question():
    task2_llm = llm2.with_structured_output(IELTSTask2)
    random_topic = random.choice(TASK2_TOPICS)
    random_question_type = random.choice(TASK2_QUESTION_TYPES)
    some_keywords = random.choices(TASK2_TOPICS_KEYWORDS[random_topic], k=3)
    keywords_str = ", ".join(some_keywords)
    task2_question = task2_llm.invoke(f"Generate an IELTS Task 2 question on the topic of {random_topic}, {random_question_type}, and include the following keywords: {keywords_str}")
    return task2_question

def score_task1_essay(essay: str, task1_data: dict):
    CC_llm = llm2.with_structured_output(IELTSTask1_Criteria_Coherence_and_Cohesion)
    LR_llm = llm2.with_structured_output(IELTSTask1_Criteria_Lexical_Resource)
    GRA_llm = llm2.with_structured_output(IELTSTask1_Criteria_Grammatical_Range_and_Accuracy)
    TA_llm = llm2.with_structured_output(IELTSTask1_Criteria_Task_Achievement)

    CC_score = CC_llm.invoke(f"Score the Coherence and Cohesion of the IELTS Task 1 essay: {essay}")
    LR_score = LR_llm.invoke(f"Score the Lexical Resource of the IELTS Task 1 essay: {essay}")
    GRA_score = GRA_llm.invoke(f"Score the Grammatical Range and Accuracy of the IELTS Task 1 essay: {essay}")
    TA_score = TA_llm.invoke(f"Score the Task Achievement of the IELTS Task 1 essay: {essay}")

    return_data = {
        "Coherence and Cohesion": CC_score.task1_criteria_coherence_and_cohesion,
        "Lexical Resource": LR_score.task1_criteria_lexical_resource,
        "Grammatical Range and Accuracy": GRA_score.task1_criteria_grammatical_range_and_accuracy,
        "Task Achievement": TA_score.task1_criteria_task_achievement,
        "Feedback": {
            "Coherence and Cohesion": CC_score.task1_criteria_coherence_and_cohesion_feedback,
            "Lexical Resource": LR_score.task1_criteria_lexical_resource_feedback,
            "Grammatical Range and Accuracy": GRA_score.task1_criteria_grammatical_range_and_accuracy_feedback,
            "Task Achievement": TA_score.task1_criteria_task_achievement_feedback
        },
        "Task 1 Data": {
            "Task 1 Description": task1_data.task1_description,
        },
        "Task 1 Essay": essay,
        "overall_score": (CC_score.task1_criteria_coherence_and_cohesion + LR_score.task1_criteria_lexical_resource + GRA_score.task1_criteria_grammatical_range_and_accuracy + TA_score.task1_criteria_task_achievement) / 4
    }
    
    return return_data

def score_task2_essay(essay: str, task2_data: dict):
    TA_llm = llm2.with_structured_output(IELTSTask2_Criteria_Task_Achievement)
    CC_llm = llm2.with_structured_output(IELTSTask2_Criteria_Coherence_and_Cohesion)
    LR_llm = llm2.with_structured_output(IELTSTask2_Criteria_Lexical_Resource)
    GRA_llm = llm2.with_structured_output(IELTSTask2_Criteria_Grammatical_Range_and_Accuracy)

    TA_score = TA_llm.invoke(f"Score the Task Achievement of the IELTS Task 2 essay: {essay}")
    CC_score = CC_llm.invoke(f"Score the Coherence and Cohesion of the IELTS Task 2 essay: {essay}")
    LR_score = LR_llm.invoke(f"Score the Lexical Resource of the IELTS Task 2 essay: {essay}")
    GRA_score = GRA_llm.invoke(f"Score the Grammatical Range and Accuracy of the IELTS Task 2 essay: {essay}")

    return_data = {
        "Task Achievement": TA_score.task2_criteria_task_achievement,
        "Coherence and Cohesion": CC_score.task2_criteria_coherence_and_cohesion,
        "Lexical Resource": LR_score.task2_criteria_lexical_resource,
        "Grammatical Range and Accuracy": GRA_score.task2_criteria_grammatical_range_and_accuracy,
        "Feedback": {
            "Task Achievement": TA_score.task2_criteria_task_achievement_feedback,
            "Coherence and Cohesion": CC_score.task2_criteria_coherence_and_cohesion_feedback,
            "Lexical Resource": LR_score.task2_criteria_lexical_resource_feedback,
            "Grammatical Range and Accuracy": GRA_score.task2_criteria_grammatical_range_and_accuracy_feedback
        },
        "Task 2 Data": {
            "Task 2 Topic": task2_data.task2_topic,
            "Task 2 Question": task2_data.task2_question
        },
        "Task 2 Essay": essay,
        "overall_score": (TA_score.task2_criteria_task_achievement + CC_score.task2_criteria_coherence_and_cohesion + LR_score.task2_criteria_lexical_resource + GRA_score.task2_criteria_grammatical_range_and_accuracy) / 4
    }

    return return_data

def calculate_overall_score(task1_scores: dict, task2_scores: dict):
    overall_score = (task1_scores["Coherence and Cohesion"] + task1_scores["Lexical Resource"] + task1_scores["Grammatical Range and Accuracy"] + task1_scores["Task Achievement"] + task2_scores["Task Achievement"] + task2_scores["Coherence and Cohesion"] + task2_scores["Lexical Resource"] + task2_scores["Grammatical Range and Accuracy"]) / 8
    # 6.25 -> 6.5, 6.75 -> 7
    overall_score = round(overall_score * 2) / 2

    return overall_score

def save_practice_data(task1_data: dict, task2_data: dict, overall_score: float, time_taken: float):
    collection = db_client['writing_king']['practices']
    data = {
        "date": datetime.now(),
        "task1_data": task1_data,
        "task2_data": task2_data,
        "overall_score": overall_score,
        "time_taken": time_taken
    }
    collection.insert_one(data)

    collection2 = db_client['writing_king']['practice_stats']
    practice_stats = list(collection2.find())
    if practice_stats:
        practice_stats = practice_stats[0]
        practice_stats['total_practice_times'] += 1
        practice_stats['total_task1_practice_times'] += 1
        practice_stats['total_task2_practice_times'] += 1
        practice_stats['all_task1_practice_scores'].append(task1_data['overall_score'])
        practice_stats['all_task2_practice_scores'].append(task2_data['overall_score'])
        collection2.update_one({}, {"$set": practice_stats})
    else:
        practice_stats = {
            "total_practice_times": 1,
            "total_task1_practice_times": 1,
            "total_task2_practice_times": 1,
            "all_task1_practice_scores": [task1_data['overall_score']],
            "all_task2_practice_scores": [task2_data['overall_score']]
        }
        collection2.insert_one(practice_stats)


def practice():
    time_s = time.time()
    st.title("IELTS Writing Practice")

    with st.form(key='ielts_form'):
        tab1, tab2 = st.tabs(["Task 1", "Task 2"])

        with tab1:
            task1_data,task1_data_type = generate_task1_question()
            task1_description = task1_data.task1_description
            
            st.write(f"{task1_description}")
            st.write(f"Data Type: {task1_data_type}")
            
            if task1_data_type == "line": # line chart
                task1_line_data_category = task1_data.task1_line_data_category
                task1_x_y_labels = task1_data.task1_line_x_y_labels
                fig = go.Figure()
                for i in range(len(task1_data.task1_line_data_y)):
                    fig.add_trace(go.Scatter(x=task1_data.task1_line_data_x, y=task1_data.task1_line_data_y[i], mode='lines', name=task1_line_data_category[i]))

                fig.update_layout(title="Task 1 Data", xaxis_title=task1_x_y_labels[0], yaxis_title=task1_x_y_labels[1])
                st.plotly_chart(fig)

            else:
                st.write("Data type not supported.")
            
            t1_essay = st.text_area("Enter your IELTS Task 1 essay here:")

        with tab2:
            task2_data = generate_task2_question()
            task2_topic = task2_data.task2_topic
            task2_question = task2_data.task2_question

            st.write(f"Task 2 Topic: {task2_topic}")
            st.write(f"Task 2 Question: {task2_question}")
            # st.write("Task 2: Write an essay on the given topic.")
            t2_essay = st.text_area("Enter your IELTS Task 2 essay here:")

        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        time_taken = time.time() - time_s
        task1_scores = score_task1_essay(t1_essay, task1_data)
        task2_scores = score_task2_essay(t2_essay, task2_data)
        overall_score = calculate_overall_score(task1_scores, task2_scores)
        save_practice_data(task1_scores, task2_scores, overall_score, time_taken)
        st.success(f"Practice submitted successfully! Your overall score is: {overall_score}")