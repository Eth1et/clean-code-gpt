export interface User {
    id: string;
    username: string;
    email: string;
    name: {
        firstName: string;
        lastName: string;
    };
}