package yao.onlinerecord.mapper;

import org.springframework.beans.factory.parsing.Problem;

import java.util.List;

public interface ProblemsMapper {
    public default List<Problem> selectByProblemId(Integer problem_id){

        return null;
    }
}
