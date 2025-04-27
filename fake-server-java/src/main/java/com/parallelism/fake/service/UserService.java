package com.parallelism.fake.service;

import com.parallelism.fake.dto.DataUser;
import com.parallelism.fake.enums.EnumUserDetails;
import com.parallelism.fake.dto.UserDetailsDTO;
import com.parallelism.fake.entity.User;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.parallelism.fake.repository.UserRepository;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;

    @Autowired
    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public List<User> getAllUsers() {
        return userRepository.findAll();
    }

    public Optional<User> getUserById(Long id) {
        return userRepository.findById(id);
    }

    // Add to UserService.java
    public DataUser getUserDetailsByEmail(String email) throws
                                                        Exception {
        Optional<User> user = userRepository.findByEmail(email);

        if (user.isPresent()) {
            String userEmail = user.get()
                                   .getEmail();

            if ("alice@example.com".equals(userEmail)) {
                return new DataUser(new UserDetailsDTO(25, "Paris"));
            } else if ("bob@example.com".equals(userEmail)) {
                return new DataUser(new UserDetailsDTO(30, "Lyon"));
            }
        }

        throw new Exception(EnumUserDetails.NOT_EXIST.TEXT);
    }
}
