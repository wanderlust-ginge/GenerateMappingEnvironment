# HOW TO USE

* These files can be placed in any project you'd like to use them in.  Just maintain the folder structure. 

* To add to an existing project, in `GenerateMappingEnvironment.py`:
    * delete lines 114-116
    * Double check the defaul GitHubRepo class will work for you.  If not, change what you need
    * Make sure you pass in the correct args.  
        * dir_name should be the parent of the App repo
        * app_name should be the name of the App, and thus assumed of its repo

* If you just want to test it on one app dir, then you can leave the last few lines in and change the default args in line 27 to match what you need.

# WHY IS THIS USEFUL?

* It's going to help you auto create a mapping enviornment by:
    * Maintaining the App.Mapper files structure that's expected by Starcounter
    * Adding the `shared` submodule in the expected place
    * Auto creating the required `AppName.Mapper.csproj` file and adding it to the main `App.sln` file
    * Making your life happier and more bug free.  You're welcome.