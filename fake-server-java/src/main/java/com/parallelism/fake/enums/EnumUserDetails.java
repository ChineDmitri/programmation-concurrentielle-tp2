package com.parallelism.fake.enums;

public enum EnumUserDetails {

    NOT_EXIST("Utilisateur n'éxiste pas");

    public final String TEXT;

    private EnumUserDetails(String label) {
        this.TEXT = label;
    }
}
