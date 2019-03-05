Angular Tutorial里的测试坑
===
发现[Angular Tutorial](https://angular.io/tutorial)里根本没有提到Unit Test，其实我们每generate一个component，就会自动生成unit test spec，作为一个资深强迫症攻城狮，实在不能视而不见。

按照[Angular Tutorial](https://angular.io/tutorial)里的step，每增加一个功能，基本上会有一些test case会fail，虽然程序运行正常。主要是因为使用`ng generate component`时，会把新Module加入app.module.ts，但是却不会更新Unit Test。其他组件fail的原因也类似。

# app-&lt;component&gt; is not a known element
`app-heros`代码敲完后，页面显示正常，单元测试却报错如下。
```bash
 Error: Template parse errors:
        'app-heros' is not a known element:
        1. If 'app-heros' is an Angular component, then verify that it is part of this module.
        2. If 'app-heros' is a Web Component then add 'CUSTOM_ELEMENTS_SCHEMA' to the '@NgModule.schemas' of this component to suppress this message. 
```

解决办法有两种。

直觉Mock才是好方法，不过有待证实。

因为后面会继续增加很多component，所以直接declare比较简单。

## 1. 导入HerosComponent
```js
import { HerosComponent } from './heros/heros.component';

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        HerosComponent
      ],
    }).compileComponents();
  }));

```
## 2. Mock HerosComponent
```js
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        MockHerosComponent
      ],
    }).compileComponents();
  }));

@Component({
  selector: 'app-heros',
  template: ''
})
class MockHerosComponent{
}
```

## 其他Component
添加其他Component的时候也是一样，会遇到类似的错。
- app-heroes (HeroesComponent)
- app-messages (MessagesComponent)
- app-hero-detail (HeroDetailComponent)
- router-outlet (AppRoutingModule)
- app-dashboard (DashboardComponent)
- app-hero-search (HeroSearchComponent)

解决方法类似，如`app-hero-detail`报错，即需要declare `HeroDetailComponent`。

```bash
Error: Template parse errors:
Can't bind to 'hero' since it isn't a known property of 'app-hero-detail'.
1. If 'app-hero-detail' is an Angular component and it has 'hero' input, then verify that it is part of this module.
2. If 'app-hero-detail' is a Web Component then add 'CUSTOM_ELEMENTS_SCHEMA' to the '@NgModule.schemas' of this component to suppress this message.
3. To allow any property add 'NO_ERRORS_SCHEMA' to the '@NgModule.schemas' of this component. ("
</ul>
```

## The module has not been imported
以下错误也一样，把相应Module放进declarations即可。
```
Failed: Component DashboardComponent is not part of any NgModule or the module has not been imported into your module.
```
# router-outlet is not a known element
`router-outlet`的情况有些特别，因为是RouterModule，所以AppRoutingModule需要放到imports下，而不是declarations里，与下面FormsModule一样。

```bash
Failed: Template parse errors:
'router-outlet' is not a known element:
1. If 'router-outlet' is an Angular component, then verify that it is part of this module.
2. If 'router-outlet' is a Web Component then add 'CUSTOM_ELEMENTS_SCHEMA' to the '@NgModule.schemas' of this component to suppress this message. ("
  </nav>
  <!-- <app-heroes></app-heroes> -->
  [ERROR ->]<router-outlet></router-outlet>
  <app-messages></app-messages>
<!-- </div> -->
"): ng:///DynamicTestModule/AppComponent.html@9:2
```

但是AppRoutingModule是路由，import AppRoutingModule将导致子模块须引入更多其他不相关模块，所以不能作为解决方案。

还好Angular提供了RouterTestingModule。Import RouterTestingModule， 错误消失。
```js
import { RouterTestingModule } from '../../../node_modules/@angular/router/testing';
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule, HttpClientTestingModule],
      declarations: [HeroSearchComponent]
    })
      .compileComponents();
  }));
```

# Can't bind to 'routerLink' 
 `routerLink`类似于`router-outlet`。
```bash
Failed: Template parse errors:
Can't bind to 'routerLink' since it isn't a known property of 'a'. ("
<ul class="heroes">
  <li *ngFor="let hero of heroes">
    <a [ERROR ->]routerLink="/detail/{{hero.id}}">
      <span class="badge">{{hero.id}}</span> {{hero.name}}
    </a>"): ng:///DynamicTestModule/HeroesComponent.html@13:7
```

Solution: Imports RouterTestingModule.
```js
import { RouterTestingModule } from '@angular/router/testing';

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([{ path: 'heroes', component: HeroesComponent }]),
        HttpClientTestingModule ],
      declarations: [ HeroesComponent ]
    })
    .compileComponents();
  }));
```

# No base href set
这个错会在刚开始用AppRoutingModule时遇到。因为我们很自然会想到要在test case里import AppRoutingModule。
```bash
Error: No base href set. Please provide a value for the APP_BASE_HREF token or add a base element to the document.
```

TestBed.configureTestingModule加以下configure可以解决。
```
providers: [{provide: APP_BASE_HREF, useValue: '/' }]
```
但更简单的做法是把测试里的AppRoutingModule替换为
RouterTestingModule。

```js
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        HeroesComponent,
        MessagesComponent,
        HeroDetailComponent,
        DashboardComponent,
        HeroSearchComponent
      ],
      imports: [
        FormsModule,
        // AppRoutingModule
        RouterTestingModule
      ]
      // providers: [{provide: APP_BASE_HREF, useValue: '/' }]
    }).compileComponents();
  }));
```
# Can't bind to 'ngModel' 
页面使用到`ngModel`时，控件绑定需要import FormsModule。这个教程里也有提到，但是只是针对app.module.ts，其实Test Case里也要。

```bash
Failed: Template parse errors:
Can't bind to 'ngModel' since it isn't a known property of 'input'. ("
  <div>
    <label>name:
      <input [ERROR ->][(ngModel)]="hero.name" placeholder="name"/>
    </label>
  </div>
"): ng:///DynamicTestModule/HeroDetailComponent.html@6:13
```

Solution: Imports FormsModule.
```js
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [ FormsModule, 
        RouterTestingModule.withRoutes([{ path: 'detail/:id', component: HeroDetailComponent }]),
        HttpClientTestingModule ],
      declarations: [ HeroDetailComponent ]
    })
    .compileComponents();
  }));
```

# Error: StaticInjectorError
这个错出现在引入`angular-in-memory-web-api`模拟server response的时候。HeroService需要注入HttpClient。

```bash
Error: StaticInjectorError(DynamicTestModule)[HttpClient]: 
  StaticInjectorError(Platform: core)[HttpClient]: 
    NullInjectorError: No provider for HttpClient!
```

Solution: Imports HttpClientTestingModule.

```js
import { HttpClientTestingModule } from '@angular/common/http/testing';

imports: [ FormsModule, 
        RouterTestingModule.withRoutes([{ path: 'heroes', component: HeroesComponent }]),
        HttpClientTestingModule ],
```

# 示例代码
## app.component.spec.ts
```js
import { TestBed, async } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { HeroesComponent } from './heroes/heroes.component';
import { MessagesComponent } from './messages/messages.component';
// import { AppRoutingModule } from './app-routing.module';

import { HeroDetailComponent } from './hero-detail/hero-detail.component';

import { FormsModule } from '@angular/forms';
// import {APP_BASE_HREF} from '@angular/common';
import { DashboardComponent } from './dashboard/dashboard.component';
import { HeroSearchComponent } from './hero-search/hero-search.component';
import { RouterTestingModule } from '../../node_modules/@angular/router/testing';

describe('AppComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        AppComponent,
        HeroesComponent,
        MessagesComponent,
        HeroDetailComponent,
        DashboardComponent,
        HeroSearchComponent
      ],
      imports: [
        FormsModule,
        // AppRoutingModule
        RouterTestingModule
      ]
      // providers: [{provide: APP_BASE_HREF, useValue: '/' }]
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Tour of Heroes'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('Tour of Heroes');
  });

  it('should render title in a h1 tag', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('h1').textContent).toContain('Tour of Heroes');
  });
});

// @Component({
//   selector: 'app-heros',
//   template: ''
// })
// class MockHeroesComponent{
// }
```

## dashboard.component.spec.ts
```js
import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DashboardComponent } from './dashboard.component';

import { RouterTestingModule } from '@angular/router/testing';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { HeroSearchComponent } from '../hero-search/hero-search.component';

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule.withRoutes([{ path: 'dashboard', component: DashboardComponent }]),
        HttpClientTestingModule],
      declarations: [DashboardComponent, HeroSearchComponent]
    })
      .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});

```

# Reference
https://angular.io/tutorial   
https://stackblitz.com/angular/xedbpmlyaag?file=src%2Fapp%2Fapp.module.ts   
https://angular.io/api/router/testing/RouterTestingModule