import { User } from "./User";

export interface Comment {
  forumId: number;
  sender: User;
  date: firebase.firestore.Timestamp;
  message: string;
}