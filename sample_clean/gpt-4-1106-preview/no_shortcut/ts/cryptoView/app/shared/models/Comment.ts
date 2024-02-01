import firebase from "firebase/app";
import { User } from "./User";

export interface ForumComment {
    forumId: number;
    sender: User;
    timestamp: firebase.firestore.Timestamp;
    message: string;
}