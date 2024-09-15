import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort, send_file
from werkzeug.utils import secure_filename
from flask_migrate import Migrate
from models import db, Content, Analytics, Tag, content_tags
from datetime import datetime
from utils import generate_short_url, get_file_type
import config

app = Flask(__name__)
app.config.from_object(config.Config)

db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    # Query for the most recent contents (adjust the limit as needed)
    recent_contents = Content.query.order_by(
        Content.created_at.desc()).limit(10).all()

    # Query for all tags (for the filter)
    tags = Tag.query.order_by(Tag.name).all()

    return render_template('index.html', contents=recent_contents, tags=tags)


def time_ago(dt):
    now = datetime.now()
    diff = now - dt

    if diff.days > 365:
        return f"{diff.days // 365} year{'s' if diff.days >= 730 else ''} ago"
    if diff.days > 30:
        return f"{diff.days // 30} month{'s' if diff.days >= 60 else ''} ago"
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days > 1 else ''} ago"
    if diff.seconds > 3600:
        return f"{diff.seconds // 3600} hour{'s' if diff.seconds >= 7200 else ''} ago"
    if diff.seconds > 60:
        return f"{diff.seconds // 60} minute{'s' if diff.seconds >= 120 else ''} ago"
    return "just now"


# Register the custom filter
app.jinja_env.filters['time_ago'] = time_ago


@app.route('/upload', methods=['POST'])
def upload():
    try:
        content_type = request.form.get('content_type')
        content = request.form.get('content')
        file = request.files.get('file')
        tags = request.form.getlist('tags')

        if content_type not in ['text', 'image', 'video']:
            return jsonify({'error': 'Invalid content type'}), 400

        if content_type == 'text':
            if not content:
                return jsonify({'error': 'No content provided'}), 400
            file_path = None
            file_type = None
        elif file:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
            file_type = get_file_type(file.filename)
        else:
            return jsonify({'error': 'No file provided'}), 400

        short_url = generate_short_url()

        new_content = Content(content_type=content_type,
                              content=content,
                              file_path=file_path,
                              short_url=short_url,
                              file_type=file_type,
                              views=0,
                              shares=0)

        # Add tags
        for tag_name in tags[:3]:  # Limit to 3 tags
            tag = Tag.query.filter_by(name=tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
            new_content.tags.append(tag)

        db.session.add(new_content)
        db.session.commit()

        return jsonify({'short_url': short_url})

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred'}), 500


@app.route('/<short_url>')
def view_content(short_url):
    content = Content.query.filter_by(short_url=short_url).first_or_404()
    if content.views is None:
        content.views = 0
    content.views += 1
    db.session.add(Analytics(content_id=content.id, action_type='view'))
    db.session.commit()
    return render_template('view.html', content=content)


@app.route('/raw/<short_url>')
def raw_content(short_url):
    content = Content.query.filter_by(short_url=short_url).first_or_404()
    if content.content_type == 'text':
        return content.content
    elif content.file_path:
        return send_file(content.file_path)
    else:
        abort(404)


@app.route('/wall')
def wall():
    tag_filter = request.args.get('tag')
    if tag_filter:
        contents = Content.query.join(
            Content.tags).filter(Tag.name == tag_filter).order_by(
                Content.created_at.desc()).limit(50).all()
    else:
        contents = Content.query.order_by(
            Content.created_at.desc()).limit(50).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('wall.html', contents=contents, tags=tags)


@app.route('/increment_share/<short_url>', methods=['POST'])
def increment_share(short_url):
    content = Content.query.filter_by(short_url=short_url).first_or_404()
    if content.shares is None:
        content.shares = 0
    content.shares += 1
    db.session.add(Analytics(content_id=content.id, action_type='share'))
    db.session.commit()
    return jsonify({'success': True, 'new_share_count': content.shares})


@app.route('/analytics')
def analytics():
    total_views = db.session.query(db.func.sum(Content.views)).scalar() or 0
    total_shares = db.session.query(db.func.sum(Content.shares)).scalar() or 0
    most_viewed = Content.query.order_by(
        Content.views.desc().nullslast()).limit(10).all()
    most_shared = Content.query.order_by(
        Content.shares.desc().nullslast()).limit(10).all()

    # Get tag statistics
    tag_stats = db.session.query(Tag.name, db.func.count(content_tags.c.content_id).label('count'), Tag.created_at)\
        .join(content_tags)\
        .group_by(Tag.id)\
        .order_by(db.desc('count'))\
        .limit(20)\
        .all()

    return render_template('analytics.html',
                           total_views=total_views,
                           total_shares=total_shares,
                           most_viewed=most_viewed,
                           most_shared=most_shared,
                           tag_stats=tag_stats)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
