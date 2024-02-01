import { User } from "./User";
import firebase from 'firebase';

export interface Comment {
    forumId: number;
    sender: User;
    date: firebase.firestore.Timestamp;
    message: string;
}