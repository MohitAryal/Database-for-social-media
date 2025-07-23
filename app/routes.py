from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import *
from app.schemas import *

router = APIRouter()

# --- USERS ---

@router.post("/users/", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    new_user = User(name=user.name)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/user/")
async def delete_user(payload: UserDelete, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(User)
        .options(
            selectinload(User.posts),
            selectinload(User.comments),
            selectinload(User.post_likes),
            selectinload(User.post_saves),
            selectinload(User.comment_likes)
        )
        .where(User.id == payload.id)
    )
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User and related data deleted"}



# --- POSTS ---

@router.post("/posts/", response_model=PostOut)
async def create_post(post: PostCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.id == post.user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = Post(user_id=post.user_id, content=post.content)
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post


@router.get("/posts/{post_id}", response_model=PostOut)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(Post, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/users/{user_id}/posts")
async def get_all_posts_by_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Post).where(Post.user_id == user_id)
    result = await db.execute(query)
    posts = result.scalars().all()
    return posts


@router.get("/posts/{post_id}/likes")
async def get_all_likes_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    query = select(PostLike).where(PostLike.post_id == post_id)
    result = await db.execute(query)
    likes = result.scalars().all()
    return likes


@router.get("/posts/{post_id}/comments")
async def get_all_comments_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Comment).where(Comment.post_id == post_id)
    result = await db.execute(query)
    comments = result.scalars().all()
    return comments


@router.get("/posts/{post_id}/saves")
async def get_all_saves_for_post(post_id: int, db: AsyncSession = Depends(get_db)):
    query = select(PostSave).where(PostSave.post_id == post_id)
    result = await db.execute(query)
    saves = result.scalars().all()
    return saves


@router.delete("/post/")
async def delete_post(payload: PostDelete, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Post)
        .options(
            selectinload(Post.likes),
            selectinload(Post.saves),
            selectinload(Post.comments),
            selectinload(Post.categories),
        )
        .where(Post.id == payload.id)
    )
    post = result.scalars().first()

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await db.delete(post)
    await db.commit()
    return {"message": "Post deleted"}


# --- COMMENTS ---

@router.post("/comments/", response_model=CommentOut)
async def create_comment(comment: CommentCreate, db: AsyncSession = Depends(get_db)):
    # Validate user and post
    user = await db.get(User, comment.user_id)
    post = await db.get(Post, comment.post_id)
    if not user or not post:
        raise HTTPException(status_code=404, detail="User or Post not found")

    print(comment.dict())
    new_comment = Comment(**comment.dict())
    db.add(new_comment)
    await db.commit()
    await db.refresh(new_comment)
    return new_comment


@router.get("/posts/{post_id}/comments", response_model=List[CommentOut])
async def get_comments(post_id: int, nested: bool = True, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment).where(Comment.post_id == post_id).order_by(Comment.timestamp).options(selectinload(Comment.replies))
    )
    all_comments = result.scalars().all()

    if nested:
        # Build nested structure
        comment_map = {c.id: c for c in all_comments}
        root_comments = []
        for comment in all_comments:
            if comment.reply_to:
                parent = comment_map.get(comment.reply_to)
                if parent:
                    parent.replies.append(comment)
            else:
                root_comments.append(comment)
        return root_comments
    return all_comments


@router.get("/comments/{comment_id}/details")
async def get_comment_details(comment_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Comment).options(
        selectinload(Comment.likes),
        selectinload(Comment.replies)
    ).where(Comment.id == comment_id)

    result = await db.execute(query)
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return {
        "comment_id": comment.id,
        "content": comment.content,
        "likes": comment.likes,
        "replies": comment.replies
    }


@router.delete("/comment/")
async def delete_comment(payload: CommentDelete, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Comment)
        .options(
            selectinload(Comment.replies),
            selectinload(Comment.likes)
        )
        .where(Comment.id == payload.id)
    )
    comment = result.scalars().first()

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    await db.delete(comment)
    await db.commit()
    return {"message": "Comment deleted"}


# --- COMMENT LIKES ---

@router.post("/comments/{comment_id}/like")
async def like_comment(comment_id: int, like: LikeCreate, db: AsyncSession = Depends(get_db)):
    # Check if already liked
    exists = await db.execute(
        select(CommentLike).where(
            CommentLike.comment_id == comment_id,
            CommentLike.user_id == like.user_id
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already liked")

    new_like = CommentLike(comment_id=comment_id, user_id=like.user_id)
    db.add(new_like)
    await db.commit()
    return {"message": "Comment liked"}


# --- POST LIKES ---

@router.post("/posts/{post_id}/like")
async def like_post(post_id: int, like: LikeCreate, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(
        select(PostLike).where(
            PostLike.post_id == post_id,
            PostLike.user_id == like.user_id
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already liked")
    db.add(PostLike(post_id=post_id, user_id=like.user_id))
    await db.commit()
    return {"message": "Post liked"}


@router.delete("/post/like/")
async def remove_post_like(payload: LikeRemove, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PostLike).where(PostLike.user_id == payload.user_id)
    )
    like = result.scalars().first()

    if not like:
        raise HTTPException(status_code=404, detail="Like not found")

    await db.delete(like)
    await db.commit()
    return {"message": "Like removed"}


# --- POST SAVES ---

@router.post("/posts/{post_id}/save")
async def save_post(post_id: int, save: SaveCreate, db: AsyncSession = Depends(get_db)):
    exists = await db.execute(
        select(PostSave).where(
            PostSave.post_id == post_id,
            PostSave.user_id == save.user_id
        )
    )
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already saved")
    db.add(PostSave(post_id=post_id, user_id=save.user_id))
    await db.commit()
    return {"message": "Post saved"}


@router.delete("/post/save/")
async def remove_post_save(payload: SaveRemove, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(PostSave).where(PostSave.user_id == payload.user_id)
    )
    save = result.scalars().first()

    if not save:
        raise HTTPException(status_code=404, detail="Save not found")

    await db.delete(save)
    await db.commit()
    return {"message": "Save removed"}


# --- CATEGORIES ---

@router.post("/categories/", response_model=CategoryOut)
async def create_category(cat: CategoryCreate, db: AsyncSession = Depends(get_db)):
    db_cat = Category(title=cat.title)
    db.add(db_cat)
    await db.commit()
    await db.refresh(db_cat)
    return db_cat


@router.post("/posts/categories/assign")
async def assign_categories(payload: PostCategoryAssign, db: AsyncSession = Depends(get_db)):
    # Retrieve the post
    post = await db.get(Post, payload.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    # Query the categories
    result = await db.execute(
        select(Category)
        .where(Category.id.in_(payload.category_ids))
        .options(selectinload(Category.posts)) 
    )
    categories = result.scalars().all()

    if not categories:
        raise HTTPException(status_code=404, detail="Categories not found")

    # Assign categories to post
    post.categories = categories
    await db.commit()

    return {"message": "Categories assigned to post"}
