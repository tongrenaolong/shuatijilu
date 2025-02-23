package yao.onlinerecord.result;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.io.Serializable;

@Data
@NoArgsConstructor
//@JsonInclude(JsonInclude.Include.ALWAYS) // 忽略 null 字段
public class Result implements Serializable {
    private Integer code;
//    private boolean status_code;
    private String message;
    private Object data;
    // 显式定义全参构造器
//    public Result(Integer code,boolean status_code, String message, Object data) {
//        this.code = code;
//        this.status_code = status_code;
//        this.message = message;
//        this.data = data;
//    }


    public Result(Integer code, String message, Object data) {
        this.code = code;
        this.message = message;
        this.data = data;
    }

    //    public static Result success() {
//        return new Result(true,"success",null);
//    }
    public static Result success(String message,Object data) {
        System.out.println("message: " + message);
        return new Result(200,message,data);
    }
//    public static Result error(String message) {
//        return new Result(false,message,null);
//    }
}
