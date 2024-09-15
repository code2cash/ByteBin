# ByteBin

ByteBin is a web-based content sharing platform that allows users to upload and share various types of content in a customizable feed layout.

## Features

- User content uploads (text, images, videos)
- Customizable feed layouts (3-column, 1-column, and list view)
- Individual content view pages
- Analytics dashboard
- "Wall" feature for content display
- Responsive design for various screen sizes

## Technology Stack

- Backend: Python 3.11+
- Web Framework: Flask 3.0.3
- Database: PostgreSQL (using Flask-SQLAlchemy 3.1.1)
- ORM: SQLAlchemy
- Migration: Flask-Migrate 4.0.7
- Frontend: HTML, CSS, JavaScript
- Dependency Management: Poetry
- Deployment: Configured for Replit

## Project Structure

```
├── static/
│   └── js/
│       └── main.js
├── uploads/
├── templates/
│   ├── analytics.html
│   ├── base.html
│   ├── index.html
│   ├── view.html
│   └── wall.html
├── config.py
├── main.py
├── models.py
├── utils.py
├── env.py
├── atomiic.ini
├── poetry.lock
└── pyproject.toml
```

## Setup and Installation

1. Ensure you have Python 3.11 or higher installed.

2. Clone the repository:
   ```bash
   git clone https://github.com/code2cash/bytebin.git
   cd bytebin
   ```

3. Install Poetry if you haven't already:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

4. Install dependencies using Poetry:
   ```bash
   poetry install
   ```

5. Set up environment variables:
   - Copy `.env.example` to `.env` (if it exists)
   - Fill in the required environment variables, including database connection details

6. Initialize the database:
   ```bash
   poetry run flask db upgrade
   ```

7. Run the application:
   ```bash
   poetry run flask run
   ```

8. Access the application at `http://localhost:5000`

## Configuration

- `config.py`: Contains application configuration settings
- `atomiic.ini`: Configuration for deployment or environment settings
- `.replit` and `replit.nix`: Replit-specific configuration files
- `.env`: Environment variables (make sure to keep this file out of version control)

## Development

To add new dependencies to the project:
```bash
poetry add package_name
```

To update dependencies:
```bash
poetry update
```

## Database Migrations

This project uses Flask-Migrate for database migrations. To create a new migration:

```bash
poetry run flask db migrate -m "Description of changes"
```

To apply migrations:

```bash
poetry run flask db upgrade
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License:

```
MIT License

Copyright (c) 2024 code2cash

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Contact

For any questions or concerns, please open an issue on the GitHub repository.

---

This project is hosted on Replit. Click the button below to run it:

[![Run on Replit](https://replit.com/badge/github/code2cash/bytebin)](https://replit.com/github/code2cash/bytebin)

