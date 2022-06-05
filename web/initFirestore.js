import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js';
import { getFirestore, getDocs, collection } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-firestore.js";
      // If you enabled Analytics in your project, add the Firebase SDK for Google Analytics
      //import { analytics } from 'https://www.gstatic.com/firebasejs/9.8.2/firebase-analytics.js'
  
      // Add Firebase products that you want to use
      //import { auth } from 'https://www.gstatic.com/firebasejs/9.8.2/firebase-auth.js'
      //import { firestore } from 'https://www.gstatic.com/firebasejs/9.8.2/firebase-firestore.js'
console.log(keys.firebaseConfig);
const app = initializeApp(keys.firebaseConfig);
const db = getFirestore(app);

export const trashData = () => {
    return getDocs(collection(db, "trashlocation"));
};
