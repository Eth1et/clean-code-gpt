import { Component, EventEmitter, Output, Input } from '@angular/core';
import { Router } from '@angular/router';
import { User } from '../models/User';

@Component({
  selector: 'app-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss']
})
export class MenuComponent {
  @Output() onCloseSidenav: EventEmitter<boolean> = new EventEmitter();
  @Output() onLogout: EventEmitter<boolean> = new EventEmitter();
  @Input() loggedInUser?: User | null;

  constructor(private router: Router) {}

  close(logout?: boolean) {
    this.emitCloseSidenav();
    if (logout) {
      this.emitLogout();
    }
  }

  private emitCloseSidenav() {
    this.onCloseSidenav.emit(true);
  }

  private emitLogout() {
    this.onLogout.emit(true);
  }
}