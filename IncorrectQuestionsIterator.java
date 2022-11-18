/**
 * Implements an iterator to iterate over incorrectly answered MultipleChoiceQuestion(s) stored in a
 * singly linked list defined by its head.
 */
public class IncorrectQuestionsIterator extends Object implements Iterator<MultipleChoiceQuestion> {

	private LinkedNode<MultipleChoiceQuestion> next;	// refers to a node in the singly linked list of MultipleChoiceQuestion

	/**
	 * Creates a new InCorrectQuestionsIterator to start iterating through a singly linked list storing
	 * MultipleChoiceQuestion elements
	 * 
	 * Parameters:
	 * @param startNode - pointer to the head of the singly linked list
	 * 
	 */
	public IncorrectQuestionsIterator(LinkedNode<MultipleChoiceQuestion> startNode) {
		// TODO: Implement
	}

	/**
	 * Returns true if this iteration has more MultipleChoiceQuestion(s) answered incorrectly.
	 * Specified by:
	 * hasNext in interface Iterator<MultipleChoiceQuestion>
	 * 
	 * Returns:
	 * @return true if there are more incorrect MultipleChoiceQuestion(s) in this iteration
	 * 
	 */
	public boolean hasNext() {
		// TODO: Implement
	}

	/**
	 * Returns the next incorrect MultipleChoiceQuestion in this iteration
	 * Specified by:
	 * next in interface Iterator<MultipleChoiceQuestion>
	 * 
	 * Returns:
	 * @return the next incorrect MultipleChoiceQuestion in this iteration
	 * 
	 * Throws:
	 * @throws NoSuchElementException - with a descriptive error message if there are no more incorrect
	 * @throws questions in this iteration
	 * 
	 */
	public MultipleChoiceQuestion next()                            throws NoSuchElementException {
		// TODO: Implement
	}

}
