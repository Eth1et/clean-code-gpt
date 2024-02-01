import { Component, EventEmitter, Output, Input} from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../models/User';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent{
  @Output() closeSidenav: EventEmitter<boolean> = new EventEmitter();
  @Output() logout: EventEmitter<boolean> = new EventEmitter();
  @Input() loggedInUser?: User | null;

  constructor(private router: Router){}

  close(logoutClicked?: boolean){
    this.closeSidenav.emit(true);
    if(logoutClicked){
      this.logout.emit(true);
    }
  }
}