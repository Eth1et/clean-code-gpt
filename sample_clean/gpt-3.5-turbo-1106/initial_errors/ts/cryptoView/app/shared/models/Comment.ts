import { User } from "./User";
import { Timestamp } from "firebase/firestore";

export interface Comment {
  forumId: number;
  sender: User;
  date: Timestamp;
  message: string;
}