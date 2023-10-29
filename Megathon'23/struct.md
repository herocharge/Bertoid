data
- list of {title, paragraph}

paragraph
- list of {'qas', 'sent_list', 'context', 'sent_starts'}
  
    paragraph.qas
    - list of {'url', 'id', 'answers', 'question', 'is_impossible'}
        paragraph.qas.question
        - the question
        paragraph.qas.answers
        - list of {'text', 'answer_span', 'answer_start', 'answer_starts'}
            paragraph.qas.answers.text
            - the actual answer text
            paragraph.qas.answers.answer_start
            - index in the context, where the answer starts
            paragraph.qas.answers.answer_span
            - list of indices of sentences in the sent_list that are answers
            paragraph.qas.answers.answer_starts
            - list of start indices in the context of the answer and the length of the sentence
    paragraph.sent_list
    - list of sentences
    paragraph.context
    - the context (this is equal to joining the sentence list)
    paragraph.sent_start
    - list of [start index of sentence, length of sentence]
    
    