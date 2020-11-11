
pip freeze > requirements.txt

#### Create test compress files
mkdir -p dir1/dir2
echo "Jim was here!" >> dir1/dir2/test.txt
tar -czvf unpack_test.tar.gz dir1


#### Lessons Learned
* When mocking the s3 client you must do it inside the function call or it won't 
be mocked correctly