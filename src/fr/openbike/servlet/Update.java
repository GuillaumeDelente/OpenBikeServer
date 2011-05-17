package fr.openbike.servlet;

import java.io.IOException;

import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.appengine.api.taskqueue.Queue;
import com.google.appengine.api.taskqueue.QueueFactory;
import com.google.appengine.api.taskqueue.TaskOptions;

/**
 * @author Guillaume Delente
 * 
 */
public class Update extends HttpServlet {

	/**
	 * 
	 */
	private static final long serialVersionUID = 7382589918813874814L;

	public void doGet(HttpServletRequest req, HttpServletResponse resp)
			throws IOException {
		Queue queue = QueueFactory.getQueue("update-queue");
		queue.add(TaskOptions.Builder.withUrl("/internal/updateVcub").method(
				TaskOptions.Method.GET));
	}
}
