from fastapi import Body, HTTPException, Response,status,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):

    posts =db.query(models.Post).all()
    return{"data : ": posts}

@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user : int= Depends(oauth2.get_current_user),
              limit : int = 10,skip: int =0,search:Optional[str] =""):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts= cursor.fetchall()
   # posts = db.query(models.Post ).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(
            models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # post_dicts = []
    # for post, vote_count in results:
    #     post_dict = post.__dict__
    #     post_dict['votes'] = vote_count
    #     post_dicts.append(post_dict)
    
    #.filter(models.Post.owner_id==current_user.id)
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db),current_user : int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content) VALUES (%s,%s) RETURNING *"""
    #                ,(post.title,post.content))
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int,db: Session = Depends(get_db),current_user : int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" SELECT * from posts WHERE id= %s""",(str(id)) )
    # post = cursor.fetchone()
    #,models.Post.owner_id==current_user.id
    post =db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(
        models.Vote,models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    #if post.owner_id != current_user.id: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),current_user : int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" DELETE from posts WHERE id= %s returning * """,(str(id)) )
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_posts(id:int, updated_post:schemas.PostUpdate,db: Session = Depends(get_db),current_user : int= Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title= %s, content=%s, published=%s WHERE id =%s  RETURNING *"""
    #                ,(post.title,post.content,post.published,str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query =db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()
    if post_query.first() == None:
        raise HTTPException (status_code=status.HTTP_404_NOT_FOUND,
                             detail=f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    post_query.update(updated_post.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()