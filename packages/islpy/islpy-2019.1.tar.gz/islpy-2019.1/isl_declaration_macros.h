#undef __isl_keep
#undef __isl_take
#undef __isl_give
#define __isl_keep __islpy_keep
#define __isl_take __islpy_take
#define __isl_give __islpy_give

// matches order in src/wrapper/wrap_isl.hpp
ISL_DECLARE_LIST(id)

ISL_DECLARE_LIST(val)
ISL_DECLARE_LIST(aff)
ISL_DECLARE_LIST(pw_aff)
ISL_DECLARE_LIST(constraint)

ISL_DECLARE_LIST(basic_set)
#if ISLPY_ISL_VERSION >= 15
ISL_DECLARE_LIST(basic_map)
#endif
ISL_DECLARE_LIST(set)
#if ISLPY_ISL_VERSION >= 15
ISL_DECLARE_LIST(map)
ISL_DECLARE_LIST(union_set)
#endif

ISL_DECLARE_LIST(ast_expr)
ISL_DECLARE_LIST(ast_node)

ISL_DECLARE_MULTI(aff)
ISL_DECLARE_MULTI(pw_aff)
ISL_DECLARE_MULTI(val)
ISL_DECLARE_MULTI(union_pw_aff)

ISL_DECLARE_MULTI_CMP(aff)
