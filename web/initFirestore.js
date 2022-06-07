import { initializeApp } from 'https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js';
import { getFirestore, getDocs, collection } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-firestore.js";

console.log(keys.firebaseConfig);
const app = initializeApp(keys.firebaseConfig);
const db = getFirestore(app);

export const trashData = () => {
    return getDocs(collection(db, "trashlocation"));
};
