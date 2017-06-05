import sched  # scheduler

class Timer():

    def __init__(self, rate, listener):
        self.rate = rate
        self.listeners = set()
        self.repeats = True
        self.running = False
        self.sched = sched.scheduler()
        self.add_action_listener(listener)

    def add_action_listener(self, listener):
        self.listeners.add(listener)

    def remove_action_listener(self, listener):
        self.listeners.remove(listener)

    # set/getDelay

    # set/getRepeats

    def start(self):
        for listener in self.listeners:
            self.sched.
        self.sched.run(blocking=False)

    def stop(self):
        pass

    # set/is running


        """

        @param rate The number of milliseconds between ticks
        @param listener The <code>ActionListener</code> receiving the events
        """
        public SwingTimer(int rate, ActionListener listener) {
        super(rate, listener);
    }
"""
/* Inherited method: addActionListener(listener) */
/**
 * @inherited Timer#void addActionListener(ActionListener listener)
 * Adds the specified action listener to the timer.
 */

/* Inherited method: removeActionListener(listener) */
/**
 * @inherited Timer#void removeActionListener(ActionListener listener)
 * Removes the specified action listener from the timer.
 */

/* Inherited method: setDelay(delay) */
/**
 * @inherited Timer#void setDelay(int delay)
 * Sets the timer delay in milliseconds.
 */

/* Inherited method: getDelay() */
/**
 * @inherited Timer#int getDelay()
 * Returns the timer delay.
 */

/* Inherited method: setRepeats(flag) */
/**
 * @inherited Timer#void setRepeats(boolean flag)
 * Sets whether the timer repeats or is a one-shot event.
 */

/* Inherited method: isRepeats() */
/**
 * @inherited Timer#boolean isRepeats()
 * Returns <code>true</code> if the timer repeats.
 */

/* Inherited method: start() */
/**
 * @inherited Timer#void start()
 * Starts the timer.
 */

/* Inherited method: stop() */
/**
 * @inherited Timer#void stop()
 * Stops the timer.
 */

/* Inherited method: isRunning() */
/**
 * @inherited Timer#boolean isRunning()
 * Returns <code>true</code> if the timer is running.
 */
"""
