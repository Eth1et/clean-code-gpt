import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MenuComponent } from './menu.component';

describe('MenuComponent', () => {
  let menuComponent: MenuComponent;
  let menuFixture: ComponentFixture<MenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MenuComponent ]
    }).compileComponents();

    menuFixture = TestBed.createComponent(MenuComponent);
    menuComponent = menuFixture.componentInstance;
    menuFixture.detectChanges();
  });

  it('should create the menu component', () => {
    expect(menuComponent).toBeTruthy();
  });
});