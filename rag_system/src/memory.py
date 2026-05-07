conversation_memory = []

MAX_MEMORY = 6

def add_to_memory(
    question,
    answer
):

    conversation_memory.append({

        "question": question,

        "answer": answer
    })

    #
    # Window memory
    #

    if len(
        conversation_memory
    ) > MAX_MEMORY:

        conversation_memory.pop(0)

def get_memory():

    memory_text = ""

    for turn in (
        conversation_memory
    ):

        memory_text += (
            f"User: "
            f"{turn['question']}\n"
        )

        memory_text += (
            f"Assistant: "
            f"{turn['answer']}\n\n"
        )

    return memory_text
