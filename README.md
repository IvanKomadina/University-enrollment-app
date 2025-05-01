
## 🧾 General Info

A student enrollment and course management system built with Django, supporting three distinct user roles: **administrator**, **professor**, and **student**. 
The system enables secure authentication, dynamic course enrollment, grade tracking, and user management within a university-like environment.

## 🚀 Features

### 🔐 Authentication
- Secure login for all users (admin, professor, student)
- Role-based access control
- Passwords stored using Django’s hashing system

---

### 🛠️ Administrator Role
- View and manage the full course list
- Add new courses
- Assign courses to professors
- View, add, and edit students and professors
- Manage student enrollment sheets (view/add/edit)
- View list of students for each course (via “view enrolled students” link)
- Full access to all student and course records
- **Note**: Use of Django admin panel is **not allowed** for this role

---

### 👨‍🏫 Professor Role
- View courses they are assigned to
- View list of students per course
- Modify the status of enrolled students:
  - `Enrolled` (default)
  - `Passed`
  - `Lost Signature` (e.g. failed participation)
- Students can be withdrawn **only if** their status is still `Enrolled`
- View categorized student lists:
  1. Students who lost signature
  2. Students with signature but not passed
  3. Students who passed

---

### 👨‍🎓 Student Role
- View personal enrollment sheet
- Enroll in or withdraw from available courses
- View course statuses by semester

---

## 🧱 Database Design

- Uses a custom `users` table (not Django's default `User`) with role-based foreign key to a new `roles` table (admin, professor, student)
- `courses` table includes a foreign key to the course owner (professor)
- `enrollment` table links students with courses and includes course status
- Designed to prevent assigning a non-professor as course owner

## 🖥️ Interface & Navigation

- **Admin Menu**: `Logout`, `Courses`, `Students`, `Professors`
- **Professor Menu**: `Logout`, `Courses`
- **Student Menu**: `Logout`, own enrollment sheet only

### 🗂 Enrollment Sheet View
- Split into:
  - Unenrolled courses
  - Enrolled courses by semester and status
- Actions available: Enroll, Withdraw, Mark as Passed/Lost Signature

---

## ⚙️ Technical Details

- Framework: **Django**
- Architecture: **MVT (Model–View–Template)**
