package yao.onlinerecord.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;
import yao.onlinerecord.entity.Users;
import yao.onlinerecord.result.Result;
import yao.onlinerecord.service.LoginService;
import lombok.extern.slf4j.Slf4j;
import java.util.List;

@RestController
@Slf4j
public class LoginController {
    @Autowired
    private LoginService loginService;
//    private static final Logger log = LoggerFactory.getLogger(LoginController.class);
//    @GetMapping(value="/login",  produces = "application/json;charset=UTF-8")
    @GetMapping(value="/login")
    public Result login(){
//        log.info("login running");
        List<Users> userList = loginService.list();
        for(Users user:userList){
            System.out.println("user: " + user.toString());
        }
        return Result.success("success",userList);
//        return "login";
    }
}
