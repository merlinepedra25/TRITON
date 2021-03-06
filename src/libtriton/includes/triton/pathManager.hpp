//! \file
/*
**  Copyright (C) - Triton
**
**  This program is under the terms of the Apache License 2.0.
*/

#ifndef TRITON_PATHMANAGER_H
#define TRITON_PATHMANAGER_H

#include <vector>

#include <triton/dllexport.hpp>
#include <triton/instruction.hpp>
#include <triton/modes.hpp>
#include <triton/pathConstraint.hpp>
#include <triton/symbolicExpression.hpp>
#include <triton/tritonTypes.hpp>



//! The Triton namespace
namespace triton {
/*!
 *  \addtogroup triton
 *  @{
 */

  //! The Engines namespace
  namespace engines {
  /*!
   *  \ingroup triton
   *  \addtogroup engines
   *  @{
   */

    //! The Symbolic Execution namespace
    namespace symbolic {
    /*!
     *  \ingroup engines
     *  \addtogroup symbolic
     *  @{
     */

      /*! \class PathManager
          \brief The path manager class. */
      class PathManager {
        private:
          //! Modes API.
          triton::modes::SharedModes modes;

          //! AstContext API
          triton::ast::SharedAstContext astCtxt;

        protected:
          //! \brief The logical conjunction vector of path constraints.
          std::vector<triton::engines::symbolic::PathConstraint> pathConstraints;

        public:
          //! Constructor.
          TRITON_EXPORT PathManager(const triton::modes::SharedModes& modes, const triton::ast::SharedAstContext& astCtxt);

          //! Constructor by copy.
          TRITON_EXPORT PathManager(const PathManager& other);

          //! Copies a PathManager.
          TRITON_EXPORT PathManager& operator=(const PathManager& other);

          //! Returns the size of the path constraints
          TRITON_EXPORT triton::usize getSizeOfPathConstraints(void) const;

          //! Returns the logical conjunction vector of path constraints.
          TRITON_EXPORT const std::vector<triton::engines::symbolic::PathConstraint>& getPathConstraints(void) const;

          //! Returns the logical conjunction vector of path constraints from a given range.
          TRITON_EXPORT std::vector<triton::engines::symbolic::PathConstraint> getPathConstraints(triton::usize start, triton::usize end) const;

          //! Returns the logical conjunction vector of path constraint of a given thread.
          TRITON_EXPORT std::vector<triton::engines::symbolic::PathConstraint> getPathConstraintsOfThread(triton::uint32 threadId) const;

          //! Returns the current path predicate as an AST of logical conjunction of each taken branch.
          TRITON_EXPORT triton::ast::SharedAbstractNode getPathPredicate(void) const;

          //! Returns path predicates which may reach the targeted address.
          TRITON_EXPORT std::vector<triton::ast::SharedAbstractNode> getPredicatesToReachAddress(triton::uint64 addr) const;

          //! Pushs constraints of a branch instruction to the path predicate.
          TRITON_EXPORT void pushPathConstraint(const triton::arch::Instruction& inst, const triton::engines::symbolic::SharedSymbolicExpression& expr);

          //! Pushes constraint created from node to the current path predicate.
          TRITON_EXPORT void pushPathConstraint(const triton::ast::SharedAbstractNode& node, const std::string& comment="");

          //! Pushes constraint to the current path predicate.
          TRITON_EXPORT void pushPathConstraint(const triton::engines::symbolic::PathConstraint& pco);

          //! Pops the last constraints added to the path predicate.
          TRITON_EXPORT void popPathConstraint(void);

          //! Clears the current path predicate.
          TRITON_EXPORT void clearPathConstraints(void);
      };

    /*! @} End of symbolic namespace */
    };
  /*! @} End of engines namespace */
  };
/*! @} End of triton namespace */
};

#endif /* TRITON_PATHMANAGER_H */
