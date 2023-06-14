import { defineStore } from 'pinia';

export const useToastStore = defineStore({
  id: 'toast',

  state: () => ({
    ms: 0,               // Duration of the toast message in milliseconds
    message: '',         // Message content of the toast
    classes: '',         // CSS classes for styling the toast
    isVisible: false     // Flag indicating if the toast is visible
  }),

  actions: {
    showToast(ms, message, classes) {
      this.ms = parseInt(ms);   // Convert duration to an integer
      this.message = message;   // Set the message content
      this.classes = classes;   // Set the CSS classes
      this.isVisible = true;    // Set visibility to true to show the toast

      setTimeout(() => {
        this.classes += ' -translate-y-28';   // Add a translate class to animate the toast
      }, 10);

      setTimeout(() => {
        this.classes = this.classes.replace('-translate-y-28', '');   // Remove the translate class
      }, this.ms - 500);   // Wait for the specified duration minus 500ms

      setTimeout(() => {
        this.isVisible = false;   // Hide the toast after the specified duration
      }, this.ms);
    }
  }
});
