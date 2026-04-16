# 路由設計文件 (ROUTES) - 食譜收藏夾

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 (食譜牆)** | GET | `/` | `templates/index.html` | 顯示所有公開的食譜列表 |
| **搜尋食譜** | GET | `/search` | `templates/index.html` | 根據 GET 參數 `q` 搜尋食譜並顯示 |
| **會員註冊** | GET, POST | `/auth/register` | `templates/auth/register.html` | GET: 顯示註冊表單<br>POST: 處理註冊邏輯並重導向 |
| **會員登入** | GET, POST | `/auth/login` | `templates/auth/login.html` | GET: 顯示登入表單<br>POST: 處理登入邏輯並重導向 |
| **會員登出** | POST, GET | `/auth/logout` | — | 清除 Session 並重導向至首頁 |
| **我的收藏夾** | GET | `/dashboard` | `templates/recipe/dashboard.html` | 登入限定，顯示個人建立的食譜列表 |
| **新增食譜** | GET, POST | `/recipes/create` | `templates/recipe/create.html` | GET: 顯示建立表單<br>POST: 接收表單並存入 DB |
| **食譜詳情** | GET | `/recipes/<int:id>` | `templates/recipe/detail.html` | 顯示單一食譜內容 (公開或擁有者) |
| **編輯食譜** | GET, POST | `/recipes/<int:id>/edit` | `templates/recipe/create.html` | GET: 顯示編輯表單<br>POST: 更新資料庫 |
| **刪除食譜** | POST | `/recipes/<int:id>/delete` | — | 刪除後重導向至我的收藏夾 |
| **切換公開狀態** | POST | `/recipes/<int:id>/toggle` | — | 切換食譜的 `is_public` 狀態 |

---

## 2. 每個路由的詳細說明

### Auth 模組 (auth_routes.py)

#### 1. 會員註冊 `/auth/register`
- **輸入**: GET 無參數；POST 表單包含 `username`, `email`, `password`, `confirm_password`。
- **處理邏輯**: 
  - 驗證密碼一致性與 Email 是否已被註冊。
  - 將密碼進行雜湊，呼叫 `User.create`。
- **輸出**: 成功則導向登入頁；失敗則渲染註冊頁並顯示 Flash 錯誤訊息。
- **錯誤處理**: "Email 已被使用" 等提示。

#### 2. 會員登入 `/auth/login`
- **輸入**: GET 無參數；POST 表單包含 `email`, `password`。
- **處理邏輯**: 呼叫 `User.get_by_email`，比對密碼。成功後將 `user_id` 存入 Flask Session。
- **輸出**: 成功導向 `/dashboard`；失敗回傳登入頁帶錯誤訊息。

#### 3. 會員登出 `/auth/logout`
- **輸入**: 無。
- **處理邏輯**: 清除 `session.clear()` 或是 `session.pop('user_id', None)`。
- **輸出**: 重導向至首頁。

---

### Recipe 模組 (recipe_routes.py)

#### 1. 首頁 (食譜牆) `/`
- **輸入**: 無。
- **處理邏輯**: 呼叫 `Recipe.get_all(is_public=1)`，拉出公開資料。
- **輸出**: 渲染 `index.html` 帶入食譜陣列。

#### 2. 搜尋食譜 `/search`
- **輸入**: GET 參數 `q`。
- **處理邏輯**: 以類似 `%q%` 的字串模糊搜尋食譜的 Title 或食材，並且需為公開狀態。
- **輸出**: 渲染 `index.html`。

#### 3. 我的收藏夾 `/dashboard`
- **輸入**: 無表單，取自 `session['user_id']`。
- **處理邏輯**: 若未登入則 abort(401) 或導向登入；已登入呼叫 `Recipe.get_by_user_id`。
- **輸出**: 渲染 `recipe/dashboard.html`。

#### 4. 新增食譜 `/recipes/create`
- **輸入**: POST 表單含 `title`, `image_url`, `ingredients`, `steps`, `is_public`。
- **處理邏輯**: 呼叫 `Recipe.create()`寫入。
- **輸出**: 成功回到 `/dashboard`。

#### 5. 食譜詳情 `/recipes/<int:id>`
- **輸入**: URL 中的 `id`。
- **處理邏輯**: 如果查無 `Recipe.get_by_id(id)` 回傳 404；檢查權限（必須是 `is_public=1`，或者屬於該登入使用者）。
- **輸出**: 渲染 `recipe/detail.html`。

#### 6. 編輯食譜 `/recipes/<int:id>/edit`
- **輸入**: URL 的 `id`；表單的更新值。
- **處理邏輯**: 確認是否為擁有人，POST 時呼叫 `Recipe.update` 更新覆寫。GET 返回編輯模式（複用 create.html 模板帶入初始值）。
- **輸出**: 更新成功導向 `/recipes/<id>`。

#### 7. 刪除與狀態切換 `/recipes/<int:id>/delete` 與 `/recipes/<int:id>/toggle`
- **輸入**: URL 的 `id`。
- **處理邏輯**: 檢查擁有人，呼叫 `Recipe.delete` 或 `Recipe.update(is_public=x)`。
- **輸出**: 導回 `/dashboard`。

---

## 3. Jinja2 模板清單

所有 HTML 檔案置於 `app/templates` 資料夾中。

| 模板路徑 | 說明 | 繼承自 |
| :--- | :--- | :--- |
| `base.html` | 最外層的母版（包含 Navbar、Footer 與共用 CSS/JS 引入） | - |
| `index.html` | 首頁與搜尋結果，公開的食譜牆 | `base.html` |
| `auth/login.html` | 登入表單 | `base.html` |
| `auth/register.html` | 註冊表單 | `base.html` |
| `recipe/dashboard.html` | 個人收藏列表（含編輯/刪除/新增按鈕） | `base.html` |
| `recipe/create.html` | 新增/編輯通用的表單頁面 | `base.html` |
| `recipe/detail.html` | 單一食譜圖文詳細頁 | `base.html` |
