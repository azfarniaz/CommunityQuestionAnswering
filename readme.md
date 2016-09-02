##SemEval 2017 Task 3
***

###Tasks
From the SemEval Site:
> Our main CQA task, as in 2016, is:
> “given (i) a new question and (ii) a large collection of question-answer threads created by a user community, rank the 
> answer posts that are most useful for answering the new question.”

> Additionally, we propose two sub-tasks:

> [1] Question Similarity (QS): given the new question and a set of related questions from the collection, rank the similar 
> questions according to their similarity to the original question (with the idea that the answers to the similar
> questions should be answering the new question as well).

> [2] Relevance Classification (RC): given a question from a question-answer thread, rank the answer posts according to 
> their relevance with respect to the question.

***
####SubTasks

	* **Subtask A: Question-Comment Similarity**
		> Given a question and its first 10 comments in the question thread, **rerank** these 10 comments **according to 
		> their relevance with respect to the question**. 
	* **Subtask B: Question-Question Similarity**
		> Given a new question (aka original question) and the set of the first 10 related questions (retrieved by a 
		> search engine), **rerank** the related questions according to their similarity **with respect to the original 
		> question**.
	* **Subtask C: Question-External Comment Similarity**  *-- this is the main English subtask.*
		> Given a new question (aka the original question),
		> the set of the first 10 related questions (retrieved by a search engine), each associated with its first 10 
		> comments appearing in its thread, **rerank** the 100 comments (10 questions x 10 comments) **according to their 
		> relevance with respect to the original question**.
	* **Multi-Domain Duplicate Detection Subtask (CQADupStack Task)** - *Task E: Identify duplicate questions in StackExchange.*
		> Given a new question (aka the original question), a set of 50 candidate questions,rerank the 50 candidate 
		> questions according to their relevance with respect to the original question, and **truncate the result list** in 
		> such a way that only "PerfectMatch" questions appear in it.

###Important Dates

**From SemEval Site**

	* Mon 01 Aug 2016: Trial data ready
	* Mon 05 Sep 2016: Training data ready
	* Mon 09 Jan 2017: Evaluation start
	* Mon 30 Jan 2017: Evaluation end
	* Mon 06 Feb 2017: Results posted
	* Mon 27 Feb 2017: Paper submissions due
	* Mon 03 Apr 2017: Author notifications
	* Mon 17 Apr 2017: Camera ready submissions due

###Things to look into

**Suggestions by Professor**
	* Feature Vectors

###Links
[SemEval 2017 Task 3 Main Site](http://alt.qcri.org/semeval2017/task3/)
[SemEval Task 3 Subtasks](http://alt.qcri.org/semeval2017/task3/index.php?id=description-of-tasks)
[Word2Vec using TensorFlow](https://www.tensorflow.org/versions/r0.10/tutorials/word2vec/index.html)
[Intro to NLP( Might help fill in the gaps)](http://blog.algorithmia.com/introduction-natural-language-processing-nlp/)
[Processing Corpora with Python and the NLTK](http://www.freecode.com/articles/processing-corpora-with-python-and-the-natural-language-toolkit)
[Dan Jurafsky & Chris Manning: Natural Language Processing Youtube vids](https://www.youtube.com/playlist?list=PL6397E4B26D00A269)

####Former SemEval Projects
[SemanticZ SemEval Task 3 2016](http://m-mitchell.com/NAACL-2016/SemEval/pdf/SemEval123.pdf)

