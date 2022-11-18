/**
 * Implements an iterator to iterate over correctly answered MultipleChoiceQuestion(s) stored in a
 * singly linked list defined by its head.
 */
public class CorrectQuestionsIterator extends Object implements Iterator<MultipleChoiceQuestion> {

	private LinkedNode<MultipleChoiceQuestion> next;	// refers to a node in the singly linked list of MultipleChoiceQuestion to traverse

	/**
	 * Creates a new CorrectQuestionsIterator to start iterating through a singly linked list storing
	 * MultipleChoiceQuestion elements
	 * 
	 * Parameters:
	 * @param startNode - pointer to the head of the singly linked list
	 * 
	 */
	public CorrectQuestionsIterator(LinkedNode<MultipleChoiceQuestion> startNode) {
		// TODO: Implement
	}

	/**
	 * Returns true if this iteration has more MultipleChoiceQuestion(s) answered correctly.
	 * Specified by:
	 * hasNext in interface Iterator<MultipleChoiceQuestion>
	 * 
	 * Returns:
	 * @return true if there are more correct MultipleChoiceQuestion(s) in this iteration
	 * 
	 */
	public boolean hasNext() {
		// TODO: Implement
	}

	/**
	 * Returns the next correct MultipleChoiceQuestion in this iteration
	 * Specified by:
	 * next in interface Iterator<MultipleChoiceQuestion>
	 * 
	 * Returns:
	 * @return the next correct MultipleChoiceQuestion in this iteration
	 * 
	 * Throws:
	 * @throws NoSuchElementException - with a descriptive error message if there are no more correct
	 * @throws questions in this iteration
	 * 
	 */
	public MultipleChoiceQuestion next()                            throws NoSuchElementException {
		// TODO: Implement
	}

}
