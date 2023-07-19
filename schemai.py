import openai
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

if 'selections' not in st.session_state:
    st.session_state.selections = []
if "texts" not in st.session_state:
    st.session_state.texts = []
if 'ai_responses' not in st.session_state:
    st.session_state.responses = []
if 'expanders' not in st.session_state:
    st.session_state.expanders = []
if 'parsed_expanders' not in st.session_state:
    st.session_state.parsed_expanders = []
if 'outputs' not in st.session_state:
    st.session_state.outputs = []
if 'parser_codes' not in st.session_state:
    st.session_state.parser_codes = []
if 'langchain_format_instructions_calls' not in st.session_state:
    st.session_state.langchain_format_instructions_calls = []
if 'instruction' not in st.session_state:
    st.session_state.instruction = []
if 'langchain_parser_outputs' not in st.session_state:
    st.session_state.langchain_parser_outputs = []


colA, colB, colC = st.columns([2,1,2])
colB.title("SCHEMAI")
tab1,tab2,tab3 = st.tabs(['INPUT + DIRECTIONS', 'AI GENERATED SCHEMES', 'CODE FOR PARSING SCHEMES'])
title_col1, title_col2, title_col3 = st.columns([1,2,1])


code_example1 = (f'{1}.The {2}.most {3}.simple {4}.use {5}.case {6}.might {7}.be {8}.etc.. ')
code_example2 = ("""\n\
employee_info = {
1001: {
    "name": "John Smith",
    "department": "Marketing",
    "position": "Manager",
    "salary": 50000,
    "projects": ["Project A", "Project B"]
},
1002: {
    "name": "Jane Doe",
    "department": "HR",
    "position": "HR Specialist",
    "salary": 40000,
    "projects": ["Project C"]
},
1003: {
    "name": "Mike Johnson",
    "department": "Finance",
    "position": "Accountant",
    "salary": 45000,
    "projects": ["Project B", "Project D"]
    }
}""")

# generate a python dictionary for a 

about_bar = st.sidebar
with about_bar:
    sidebar_column1, sidebar_column2, sidebar_column3 = st.columns([1,2,1])
    sidebar_column2.header("ABOUT")
    st.divider()
    st.markdown("""
    Schemai is a prototype / proof of concept for a tool that takes data in one form and transforms it into another.
    You can take a CSV file and turn it into a JSON or an XML, YAML, HTML, and many more.
    You could take this very sentence right here and turn it into a dictionary, a list, etc...
    You get the idea.""")
    st.divider()
    
    st.markdown("""There are a good number of presets in place for common data schemes as well.
    The model gives particular, special attention to the preset types. 
    I plan to continue to expand the LLM's and intensify with further learning as time goes on.
    Feel free to supply your own custom data scheme with some concsise instructions.
    As you might expect, by choosing `custom` you can also just as easily, type the format you'd like to transform the data into """)
    
    st.divider()
    
    st.markdown("""The second piece to this program is the automatic \
    generation of viable code for parsing and extracting the ai's response. \
    I believe this has the potential, if fully embraced, to create a new kind of experience we really haven't seen yet.
    A big reason why, in my opinion, is because of the well known issue of parsing unpredictivle responses.""")
    
    st.divider()
    st.markdown("""While there have been a lot of amazing solutions to the predictibility / parsing problem lately coming out from
    several places, most notably OpenAI's Python Functions, these responses merely give us a good working space with a solid
    surface to build on.""")
    
    st.divider()
    st.markdown("""By building on systems such as Langchain while utilizing the new fine-tuned functions into GPT 4 \
        this project serves as a general proof of concept.""")
    
    st.divider()
    st.subheader("""SchemAI! Save time, save brain cells... save yourself.""")
    
    st.divider()
    
    st.markdown("""(The dynamically generated parser feature currently builds the Langchain output parser in python. \
    Plans to integrate JavaScript, PHP and OpenAI functions and more is in the works).""")





# st.sidebar(f'{about}\n\n SchemAI is a tool that uses ai to translate nearly any format of data or code to nearly any other.\n\nSecondly, it recompiles your given data into a block of Langchain parsing code')                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      )

openai.api_key = st.secrets["OPENAI_API_KEY"]
chat = ChatOpenAI(temperature=0.7, verbose=True, model_name='gpt-3.5-turbo-0613', openai_api_key=openai.api_key, streaming=True)


monkey_party = """ dict | key-value pairs example: 'party-monkeys! : party monkeys api POST message'
party-level: amateur, adults: 14, ages: 34-61, monkey-experience: none, package: introduction, monkey-bar: true : type: gorilla-keg, monkey-business: true : type: pick-pockets, host: orangatang-rapper, address: 12345-unknown-street-NY-New-York-512012"""
clown_sense = """ xml example: 'clown-sense : clowns on demand api: order ticket'
<?xml version="1.0" encoding="UTF-8"?>
<clown-sense>
    <quantity>2-clowns</quantity>
    <location>little-bird-middle-school</location>
    <bullies>
        <quantity>5</quantity>
        <names>Jon_Milligan-Jillian_Hill-Jacob_Snyder-George_Milligan-Other_Na</names>
    </bullies>
    <terror-level>medium</terror-level>
    <service-description>clown-sense sends clowns to your school and will terrorize some sense into your school's bullies!</service-description>
</clown-sense>"""

show_examples = tab1.checkbox('use example data', value=False, key='examples_checkbox')
    
if show_examples:
    example_selection = tab1.selectbox('select a pre-made prompt for testing purposes', ("examples", "monkey_party", "clown_sense"))
    if example_selection == "monkey_party":
        text = tab1.text_area("you've placed an example / pre-formed prompt called 'monkey-party'", value=monkey_party)
        st.session_state.texts.append(text)
    elif example_selection == "clown_sense":
        text = tab1.text_area("You've selected to use an example prompt called 'clown-sense'", value=clown_sense)
        st.session_state.texts.append(text)
else: 
    text = tab1.text_area("place data to be formatted here")
    st.session_state.texts.append(text)
text = st.session_state.texts[-1]
selection = tab1.selectbox('select format', ('JSON', 'XML', 'CSV', 'YAML', 'TOML', 'HTML', 'CSS', 'INI', 'ProtBuf', 'Python Dictionary', 'Python Function', 'Custom' ))
if selection == 'Custom':
    custom_format = tab1.text_input('Specify A Custom Format')
    selection = custom_format
else:
    selection = selection
    
user_template = """Use the text that is delimited by triple backticks to generate your response in the format specified. \
    In it's entirety, your response should strictly adhere to the syntax and rules of the given format. \
    format: {selection} \
    text: ```{text}```\
    """

parser_prompt = """ 
Langchain is a Python library for chaining prompts with LLMs.        
A ResponseSchema defines the structure of extracted output.        
StructuredOutputParser parses text into a dict based on schemas.         
1. For each key within the data, there needs to be a defined Response Schema.The value of the `name` parameter should be the name of a given key.
2. After that, for each ResponseSchema, we place them into a python list which is stored in a variable called `response_schemas`        
3. Finally, we can define the `StructuredOutputParser`        
Your full and complete response should look something like this:
```
from langchain.output_parsers import ResponseSchema, StructuredOutputParser        
price_value_schema = ResponseSchema(name="price_value",
                            description="Extract any\
                            sentences about the value or \
                            price, and output them as a \
                            comma separated Python list.")                                    
# other ResponseSchema's, one for each key found in the dataset
response_schemas = [price_value_schema, # other schemas if they existed ] 
parser = StructuredOutPutParser.from_response_schemas(response_schemas) # this line of code should look exactly 'as is'.
```
NOTE: No need to explain what you are doing. Just provide the code block as directed.
Now given this dataset:
{schema}
Generate the ResponseSchemas and the StructuredOutPutParser...
"""        
               
auto_instructions_prompt="""Langchain is a Python library for chaining prompts with LLMs.        
1. Generate a `prompt_template` from a data set of `ResponseSchemas` that creates a set of instructions for parsing.        
2. For each `name` within the dataset, specify the `name` as a key along with instructions on how to parse.        
3. Describe a coherent and sensible way to extract the keys. Try and be more articulate than the `description` given.        
4. Include in your prompt, the  `text: {{text}}` to allow an input value to be passed in.        
5. Include `{{instructions}}` to allow a set of instructions to be passed in.
Here is an example for a prompt where 3 keys were found within a JSON dataset (gift, delivery and price_value):
```
from langchain.prompts import ChatPromptTemplate        
prompt_template = \"\"\"
From the `text`, extract the following information:
gift: Was the item purchased as a gift for someone else? \\
Answer True if yes, False if not or unknown.
delivery_days: How many days did it take for the product \\
to arrive? If this information is not found, output -1.
price_value: Extract any sentences about the value or price,\\
and output them as a comma separated Python list.        
text: {{text}}
{{format_instructions}}
\"\"\"
``` # your response should end on this line
IMPORTANT: note how we define the `prompt_template`. Please do so in the same exact manner as in the above example. 
IMPORTANT_2: your response should resemble the example above. Do not explain, comment or otherwise write any directions. Just respond with a code block as specified.
dataset: {response_schemas}
"""

langchain_format_instructions_call = """format_instructions = parser.get_format_instructions()"""

langchain_parser_output = """chat_template = ChatPromptTemplate(template = prompt_template)\nmessages = auto_instructions_prompt.format_messages(text=text, format_instructions=format_instructions)\nresponse = chat(messages)\noutput_dict = parser.parse(response.content)"""

prompt_template = ChatPromptTemplate.from_template(user_template)
user_message_template = prompt_template.format_messages(text=text, selection=selection)
parser_prompt_template = ChatPromptTemplate.from_template(parser_prompt)        
instructions_template = ChatPromptTemplate.from_template(auto_instructions_prompt)
col1, col2, col3 = tab1.columns([3,3,2])



generate_schema_button = col3.button("MAKE " + f'{selection}')

if generate_schema_button:
    
    if text is not None:
        full_response = chat(user_message_template)
        ai_response = full_response.content

        st.session_state.selections.append(selection)
        st.session_state.texts.append(text)
        st.session_state.responses.append(ai_response)
        st.session_state.expanders.append(
            {
            'selection' : selection,
            'text' : text,
            'response' : ai_response
            }
        )
        
        for expander in st.session_state.expanders:
            with tab2.expander(f"{expander['selection']}", expanded=False):
                st.markdown("**YOUR MESSAGE**")
                st.write(expander["text"])
                st.divider()
                st.markdown("**AI RESPONSE**")
                response_text = expander["response"].replace('```', '')
                st.code(response_text)
        
        formatted_parser_prompt_template = parser_prompt_template.format_messages(schema = ai_response)
        ai_parser_code = chat(formatted_parser_prompt_template)
        parser_code = ai_parser_code.content
        formatted_template_instructions = instructions_template.format_messages(response_schemas = parser_code)
        ai_instructions_template = chat(formatted_template_instructions)
        instructions = ai_instructions_template.content
        
        st.session_state.parser_codes.append(parser_code)
        st.session_state.langchain_format_instructions_calls.append(langchain_format_instructions_call)
        st.session_state.instruction.append(instructions)
        st.session_state.langchain_parser_outputs.append(langchain_parser_output)
        st.session_state.parsed_expanders.append(
            {
            'selection' : selection,
            'code' : f"{parser_code}\n{langchain_format_instructions_call}\n\n{instructions}\n{langchain_parser_output}"
            }
        )
        
        for parsed_expander in st.session_state.parsed_expanders:
            with tab3.expander(f"PARSED: {parsed_expander['selection']}", expanded=False):
                fixed_code = parsed_expander["code"].replace('```', '')
                st.code(fixed_code)
            st.divider()
            
        
