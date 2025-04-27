package com.parallelism.fake.controller;

import com.parallelism.fake.dto.DataUser;
import com.parallelism.fake.dto.UserDetailsDTO;
import com.parallelism.fake.entity.User;
import com.parallelism.fake.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/users")
public class UserController {

    private final UserService userService;

    @Autowired
    public UserController(UserService userService) {
        this.userService = userService;
    }

    @GetMapping
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }

    @GetMapping("/id/{id}")
    public ResponseEntity<User> getUserById(@PathVariable Long id) {
        return userService.getUserById(id)
                          .map(ResponseEntity::ok)
                          .orElse(ResponseEntity.notFound().build());
    }

    // Add to UserController.java
    @GetMapping("/{email}")
    public ResponseEntity<DataUser> getUserDetailsByEmail(@PathVariable String email) throws
                                                                                            Exception {
        DataUser userDetails = userService.getUserDetailsByEmail(email);

        if (userDetails != null) {
            return ResponseEntity.ok(userDetails);
        } else {
            return ResponseEntity.notFound().build();
        }
    }
}
