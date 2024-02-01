import { ComponentFixture, TestBed } from '@angular/core/testing';
import { MainComponent } from './main.component';

describe('MainComponent', () => {
  let component: MainComponent;
  let fixture: ComponentFixture<MainComponent>;

  beforeEach(async () => {
    await configureTestingModule();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  async function configureTestingModule() {
    await TestBed.configureTestingModule({
      declarations: [MainComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(MainComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }
});